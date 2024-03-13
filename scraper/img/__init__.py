import io
import PIL

from PIL.Image import Image
from realesrgan_ncnn_py import Realesrgan


class ImageEditor:

    @staticmethod
    def bytes_to_image(image_data: bytes) -> Image:
        """通过bytes数据创建一个PIL.Image对象"""
        return PIL.Image.open(io.BytesIO(image_data))

    @staticmethod
    def save(image: Image | bytes, path: str) -> None:
        """保存图片"""
        if isinstance(image, bytes):
            with open(path, 'wb') as f:
                f.write(image)
        else:
            image.save(path)

    def super_resolution(self, image: Image | bytes, model=1) -> Image:
        """
        使用Realesrgan超分，如果超分失败则返回原图（如显卡不支持）

        0: realesrgan-x4plus-anime\n
        1: realesrgan-x4plus
        :param image:
        :param model: 超分模型
        :return:
        """
        if isinstance(image, bytes):
            image = self.bytes_to_image(image)

        try:
            model = 1 if model != 0 else 0
            model += 3
            realesrgan = Realesrgan(model=model)
            img = realesrgan.process_pil(image)
            return img
        except Exception:
            return image


image_editor = ImageEditor()
