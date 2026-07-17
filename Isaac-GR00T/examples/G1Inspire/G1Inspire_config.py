from external_dependencies.robocasa.robocasa.utils.robomimic.robomimic_torch_utils import lr_scheduler_from_optim_params
from gr00t.configs.data.embodiment_configs import register_modality_config
from gr00t.data.dataset.lerobot_episode_loader import LEROBOT_INFO_FILENAME
from gr00t.data.embodiment_tags import EmbodimentTag
from gr00t.data.types import ModalityConfig, ActionConfig, ActionRepresentation, ActionType, ActionFormat


G1Inspire_config = {
    "video": ModalityConfig(
        delta_indices=[0],
        modality_keys = ["ego_view"],
    ),
    "state": ModalityConfig(
        delta_indices=[0],
        modality_keys = [
            "left_arm",
            "right_arm",
            "left_hand",
            "right_hand",
            "left_leg",
            "right_leg",
            "waist"
        ],
        sin_cos_embedding_keys = [
            "left_arm",
            "right_arm",
            "left_leg",
            "right_leg",
        ]
    ),
    "action": ModalityConfig(
        delta_indices=list(range(0, 16)),
        modality_keys = [
            "left_arm",
            "right_arm",
            "left_hand",
            "right_hand",
            "waist",
            "base_height_command",
            "navigate_command",     
        ],
        action_configs = [
            # left_arm
            ActionConfig(
                rep = ActionRepresentation.RELATIVE,
                type = ActionType.NON_EEF,
                format = ActionFormat.DEFAULT,
            ),
            # right_arm
            ActionConfig(
                rep = ActionRepresentation.RELATIVE,
                type = ActionType.NON_EEF,
                format = ActionFormat.DEFAULT,
            ),
            # left_hand
            ActionConfig(
                rep = ActionRepresentation.ABSOLUTE,
                type = ActionType.NON_EEF,
                format = ActionFormat.DEFAULT,
            ),
            # right_hand
            ActionConfig(
                rep = ActionRepresentation.ABSOLUTE,
                type = ActionType.NON_EEF,
                format = ActionFormat.DEFAULT,
            ),
            # waist
            ActionConfig(
                rep = ActionRepresentation.RELATIVE,
                type = ActionType.NON_EEF,
                format = ActionFormat.DEFAULT,
            ),
            # base_height_command
            ActionConfig(
                rep = ActionRepresentation.ABSOLUTE,
                type = ActionType.NON_EEF,
                format = ActionFormat.DEFAULT,            
            ),
            # navigate_command
            ActionConfig(
                rep = ActionRepresentation.ABSOLUTE,
                type = ActionType.NON_EEF,
                format = ActionFormat.DEFAULT,
            ),
            
        ]   

    ),
    "language": ModalityConfig(
        delta_indices=[0],
        modality_keys=["annotation.human.task_description"],
    )
}

register_modality_config(G1Inspire_config, embodiment_tag=  EmbodimentTag.NEW_EMBODIMENT)