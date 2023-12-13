from ..utils import common_annotator_call, create_node_input_types
import comfy.model_management as model_management

class VooDooNode2:
    @classmethod
    def INPUT_TYPES(cls):
        # Define input types with a new slider for user_scale
        return create_node_input_types(
            user_scale=(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], {"default": "5"})
        )

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"

    CATEGORY = "TatToolkit/VooDoo"

    def execute(self, image, resolution=512, **kwargs):
        from TatToolkit.VooDoo2 import VooDoo2

        # Retrieve the user_scale value
        user_scale = int(kwargs.get("user_scale", 5))

        # Instantiate your VooDoo with the user_scale
        lines_processor = VooDoo2(user_scale=user_scale)

        # Process the image
        out = common_annotator_call(lines_processor, image, resolution=resolution)
        del lines_processor
        return (out, )

NODE_CLASS_MAPPINGS = {
    "VooDooNode2": VooDooNode2
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "VooDooNode2": "TOUCH ME BABY2"
}
