from ..utils import common_annotator_call, annotator_ckpts_path, HF_MODEL_NAME, create_node_input_types
import comfy.model_management as model_management

class PbnifyPreprocessor:
    @classmethod
    def INPUT_TYPES(cls):
        return create_node_input_types(
            # Define any input parameters your preprocessor might need
            # For example, the number of clusters
            n_clusters=(["5", "6", "7", "8", "9", "10"], {"default": "5"})
        )

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"

    CATEGORY = "TatToolkit/Billy Goncho's Wild Ride"

    def execute(self, image, resolution=512, **kwargs):
        from TatToolkit.pbnify import PbnifyPreprocessor

        # Instantiate your preprocessor
        # Use kwargs to pass any parameters it might need, like number of clusters
        n_clusters = int(kwargs.get("n_clusters", 5))
        model = PbnifyPreprocessor(n_clusters=n_clusters)

        # Process the image
        out = common_annotator_call(model, image, resolution=resolution)
        del model
        return (out, )

NODE_CLASS_MAPPINGS = {
    "PbnifyPreprocessor": PbnifyPreprocessor
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "PbnifyPreprocessor": "DIP ITTTT"
}
