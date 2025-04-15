import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from controlnet_aux import MidasDetector, HEDdetector

# Initialize ControlNet auxiliary models - with updated repo sources
def texture_load():
    print("Loading ControlNet auxiliary models...")

    try:
    # Try to load Midas depth detector
        midas = MidasDetector.from_pretrained("lllyasviel/Annotators")
        print("✓ MidasDetector loaded successfully")
    except Exception as e:
        print(f"Error loading MidasDetector: {e}")
        print("Trying alternative source...")
        try:
            midas = MidasDetector.from_pretrained("patrickvonplaten/controlnet_aux")
            print("✓ MidasDetector loaded from alternative source")
        except Exception as e:
            print(f"Failed to load MidasDetector from alternative source: {e}")
            midas = None

    try:
    # Try to load HED edge detector
        hed = HEDdetector.from_pretrained("lllyasviel/Annotators")
        print("✓ HEDdetector loaded successfully")
    except Exception as e:
        print(f"Error loading HEDdetector: {e}")
        print("Trying alternative source...")
        try:
            hed = HEDdetector.from_pretrained("patrickvonplaten/controlnet_aux")
            print("✓ HEDdetector loaded from alternative source")
        except Exception as e:
            print(f"Failed to load HEDdetector from alternative source: {e}")
            hed = None

# Skip if the auxiliary models couldn't be loaded
    if midas is None or hed is None:
        print("Failed to load one or more auxiliary models. Cannot continue with ControlNet.")
    else:
    # Initialize ControlNet models
        print("Loading ControlNet models...")

        try:
        # Try to load depth ControlNet
            controlnet_depth = ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-depth", torch_dtype=torch.float16
        )
            print("✓ Depth ControlNet loaded successfully")
        except Exception as e:
            print(f"Error loading Depth ControlNet: {e}")
            print("Trying alternative source...")
            try:
                controlnet_depth = ControlNetModel.from_pretrained(
                "runwayml/stable-diffusion-v1-5-controlnet-depth", torch_dtype=torch.float16
            )
                print("✓ Depth ControlNet loaded from alternative source")
            except Exception as e:
                print(f"Failed to load Depth ControlNet from alternative source: {e}")
                controlnet_depth = None

        try:
        # Try to load edge ControlNet
            controlnet_hed = ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-hed", torch_dtype=torch.float16
        )
            print("✓ HED ControlNet loaded successfully")
        except Exception as e:
            print(f"Error loading HED ControlNet: {e}")
            print("Trying alternative source...")
            try:
                controlnet_hed = ControlNetModel.from_pretrained(
                "runwayml/stable-diffusion-v1-5-controlnet-hed", torch_dtype=torch.float16
            )
                print("✓ HED ControlNet loaded from alternative source")
            except Exception as e:
                print(f"Failed to load HED ControlNet from alternative source: {e}")
                controlnet_hed = None

    # Skip if the ControlNet models couldn't be loaded
        if controlnet_depth is None or controlnet_hed is None:
            print("Failed to load one or more ControlNet models. Cannot continue with ControlNet pipeline.")
        else:
        # Initialize Stable Diffusion pipeline
            print("Loading Stable Diffusion pipeline...")

            try:
                pipe = StableDiffusionControlNetPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                controlnet=[controlnet_depth, controlnet_hed],
                safety_checker=None,
                torch_dtype=torch.float16
            )

            # Configure pipeline
                pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
                pipe.enable_model_cpu_offload()
                pipe.enable_vae_slicing()
                print("✓ Models loaded successfully!")

            except Exception as e:
                print(f"Error initializing Stable Diffusion ControlNet pipeline: {e}")
                print("Will need to use an alternative approach.")