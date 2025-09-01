from PIL import Image, ImageDraw, ImageFont



class AddWatermark:
    def __init__(self, img_path):
        # Open the main image and the logo
        # Create a new image with an RGBA mode to allow transparency
        self.img = Image.open(img_path).convert("RGBA")
        self.fonts = ["arial", "times", "cour", "comic", "verdana"]
        self.font = f"{self.fonts[1]}.ttf"
        self.opacity = 255
        self.angle = 0
        self.size = 40
        self.color = [255, 255, 255]
        self.position = "many"


    def add_logo(self, logo, opacity=None):
        logo = Image.open(logo).convert("RGBA")
        watermarked_image = self.img.copy()
        # Resize the logo if necessary (e.g., to 10% of the main image width)
        # Set the opacity level (0 = fully transparent, 255 = fully opaque)

        alpha = logo.getchannel("A")  # Get the alpha channel
        alpha = alpha.point(lambda p: p * self.opacity // 255)  # Scale the opacity
        logo.putalpha(alpha)


        logo_width = self.size
        logo_height = int(logo_width * logo.size[1] / logo.size[0])
        logo = logo.resize((logo_width, logo_height), Image.LANCZOS)  # Updated to Image.LANCZOS
        logo = logo.rotate(angle=self.angle)

        # Text and image dimensions
        image_width, image_height = self.img.size
        padding = 10  # Adjust padding as needed

        # Define positions
        positions = {
            "top_left": (padding, padding),
            "top_right": (image_width - logo_width - padding, padding),
            "bottom_left": (padding, image_height - logo_height - padding),
            "bottom_right": (image_width - logo_width - padding, image_height - logo_height - padding),
            "center": ((image_width - logo_width) // 2, (image_height - logo_height) // 2)
        }

        if self.position == "many":
            for r in range(20):
                for c in range(20):
                    x = c * (logo.width + 100)
                    y = r * (logo.width + 100)
                    watermarked_image.paste(logo, (x, y), logo)
        else:
            watermarked_image.paste(logo, positions[self.position], logo)
        # Show the final watermarked image
        # self.watermarked_image.show()
        watermarked_image.convert("RGB").resize((706, 714)).save("converted_image.png", format="PNG")

    def add_text(self, water_mark_text):
        # Create a transparent overlay for the watermark
        watermark_overlay = Image.new("RGBA", self.img.size, (255, 255, 255, 0))
        # Set up the font and text for the watermark
        font = ImageFont.truetype(self.font, self.size)  # Adjust font and size as needed
        text = water_mark_text

        # Initialize ImageDraw
        draw = ImageDraw.Draw(watermark_overlay)

        # Get text size to position it
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        # Text and image dimensions
        image_width, image_height = self.img.size
        padding = 10  # Adjust padding as needed

        # Define positions
        positions = {
            "top_left": (padding, padding),
            "top_right": (image_width - text_width - padding, padding),
            "bottom_left": (padding, image_height - text_height - padding),
            "bottom_right": (image_width - text_width - padding, image_height - text_height - padding),
            "center": ((image_width - text_width) // 2, (image_height - text_height) // 2)
        }

        if self.position == "many":
            for r in range(20):
                for c in range(20):
                    x = c * (text_width + 100)
                    y = r * (text_height + 100)
                    draw.text((x, y), text, font=font, fill=tuple(self.color + [self.opacity]))  # Semi-transparent white text
        else:
            draw.text(positions[self.position], text, font=font, fill=tuple(self.color + [self.opacity]))  # Semi-transparent white text

        # Rotate the watermark overlay
        rotated_watermark = watermark_overlay.rotate(self.angle, resample=Image.BICUBIC, expand=True)

        # Center the rotated watermark onto a new overlay that matches the original image size
        centered_overlay = Image.new("RGBA", self.img.size, (255, 255, 255, 0))
        offset_x = (self.img.width - rotated_watermark.width) // 2
        offset_y = (self.img.height - rotated_watermark.height) // 2
        centered_overlay.paste(rotated_watermark, (offset_x, offset_y), rotated_watermark)

        # Composite the original image with the centered rotated watermark overlay
        watermarked_image = Image.alpha_composite(self.img.convert("RGBA"), centered_overlay)

        # Convert back to RGB if saving as JPEG
        watermarked_image = watermarked_image.convert("RGB")
        watermarked_image.resize((706, 714)).save("converted_image.png", format="PNG")

    def get_size(self):
        return self.img.size

    def resize_image(self, new_width, new_height):
        self.img.resize((new_width, new_height)).convert("RGB").save("converted_image.png", format="PNG")




# if __name__ == "__main__":
#     add = AddWatermark("sticker.jpg")
#     # add.add_logo("tik-tok.png")
#     add.add_text("Abdou Company")