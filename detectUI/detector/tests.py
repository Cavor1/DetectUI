import io
import json
import tempfile
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.test import TestCase, override_settings
from PIL import Image

from detector.models import UploadedImage, Detection

#test_image
def _pil_bytes(size=(16, 16), color=(255, 0, 0), fmt="PNG"):
    img = Image.new("RGB", size, color)
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf.getvalue()

#temp_dir
@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="x")

    def _make_uploaded_image(self, name="test.png"):
        ui = UploadedImage.objects.create(user=self.user)
        ui.image.save(name, ContentFile(_pil_bytes()), save=True)
        return ui

    def test_image_saved_under_user_folder(self):
        ui = self._make_uploaded_image("cat.png")
        rel = ui.image.name  # e.g. "uploads/user_1/cat.png"
        self.assertTrue(rel.startswith(f"uploads/user_{self.user.id}/"))
        self.assertTrue(Path(settings.MEDIA_ROOT, rel).exists())

    def test_add_detections(self):
        ui = self._make_uploaded_image()
        det = Detection.objects.create(
            image=ui, inference_model="yolo", detections=[{"label": "cat", "conf": 0.9}]
        )
        self.assertEqual(ui.detections.count(), 1) #ui has one detection
        self.assertEqual(ui.detections.first().id, det.id) #it's the one created

    def test_unique_per_image_and_model(self):
        ui = self._make_uploaded_image()
        Detection.objects.create(image=ui, inference_model="yolo", detections=[])
        with self.assertRaises(IntegrityError):
            Detection.objects.create(image=ui, inference_model="yolo", detections=[])

    def test_update_or_create_creates_then_updates(self):
        ui = self._make_uploaded_image()
        det, created = Detection.objects.update_or_create(
            image=ui, 
            inference_model="yolo",
            defaults={"detections": []}
        )
        self.assertTrue(created)
        # update same pair
        det2, created2 = Detection.objects.update_or_create(
            image=ui,
            inference_model="yolo",
            defaults={"detections": [{"label": "dog", "conf": 0.8}]},
        )
        self.assertFalse(created2)
        self.assertEqual(det.id, det2.id)
        self.assertEqual(det2.detections, [{"label": "dog", "conf": 0.8}])

    def test_detections_json_accepts_none_empty_and_items(self):
        ui = self._make_uploaded_image()
        d,_ = Detection.objects.update_or_create(image=ui, inference_model="yolo", 
                                                 defaults={"detections": None},
                                                 )
        self.assertIsNone(d.detections)
        d2,_ = Detection.objects.update_or_create(image=ui, inference_model="yolo", defaults={"detections":[]})
        self.assertEqual(d2.detections, [])
        payload = [{"label": "cat", "conf": 0.91}]
        d3,_ = Detection.objects.update_or_create(image=ui, inference_model="yolo",defaults= { "detections":payload })
        self.assertEqual(d3.detections, payload)

    def test_cascade_delete_uploadedimage_deletes_detections(self):
        ui = self._make_uploaded_image()
        det = Detection.objects.create(image=ui, inference_model="yolo", detections=[])
        self.assertEqual(Detection.objects.filter(image=ui).count(), 1)
        pk = det.pk
        ui.delete()
        self.assertEqual(Detection.objects.filter(pk=pk).count(), 0)

