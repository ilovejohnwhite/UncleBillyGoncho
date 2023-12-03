from ..utils import common_annotator_call, create_node_input_types
import comfy.model_management as model_management

class LightLinesNode:
    @classmethod
    def INPUT_TYPES(cls):
        # Define input types if your processor requires any specific inputs
        return create_node_input_types()

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"

    CATEGORY = "ControlNet Preprocessors/Light Lines"

    def execute(self, image, resolution=512, **kwargs):
        from TatToolkit.lightlines import LightLines

        # Instantiate your LightLines
        lines_processor = LightLines()

        # Process the image
        out = common_annotator_call(lines_processor, image, resolution=resolution)
        del lines_processor
        return (out, )

NODE_CLASS_MAPPINGS = {
    "LightLinesNode": LightLinesNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LightLinesNode": "Light Lines"
}
