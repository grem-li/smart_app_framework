from typing import Optional, Union, List, Dict, Any

import core.logging.logger_constants as log_const
from core.basic_models.actions.basic_actions import RequirementAction, ChoiceAction, ElseAction
from core.logging.logger_utils import log
from core.model.factory import factory
from core.text_preprocessing.base import BaseTextPreprocessingResult
from core.utils.exception_handlers import exc_handler
from scenarios.scenario_models.field.field_filler_description import FieldFillerDescription
from scenarios.user.user_model import User


class RequirementFiller(RequirementAction):
    FIELD_KEY = "filler"

    def __init__(self, items: Dict[str, Any], id: Optional[str] = None):
        super(RequirementFiller, self).__init__(items, id)
        self.internal_item = self.build_internal_item()

    @factory(FieldFillerDescription)
    def build_internal_item(self):
        return self._item

    def on_extract_error(self, text_preprocessing_result, user, params=None):
        log("exc_handler: RequirementFiller failed to extract. Return None. MESSAGE: {}.".format(
            user.message.masked_value),
            user, {log_const.KEY_NAME: log_const.HANDLED_EXCEPTION_VALUE}, level="ERROR", exc_info=True)
        return None

    @exc_handler(on_error_obj_method_name="on_extract_error")
    def extract(self, text_preprocessing_result: BaseTextPreprocessingResult,
                user: User, params: Dict[str, Any] = None) -> Optional[Union[int, float, str, bool, List, Dict]]:
        return self.run(user, text_preprocessing_result, params)


class ChoiceFiller(ChoiceAction):
    FIELD_REQUIREMENT_KEY = "requirement_fillers"
    FIELD_ELSE_KEY = "else_filler"

    def on_extract_error(self, text_preprocessing_result, user, params=None):
        log("exc_handler: ChoiceFiller failed to extract. Return None. MESSAGE: {}.".format(user.message.masked_value),
            user,
            {log_const.KEY_NAME: log_const.HANDLED_EXCEPTION_VALUE}, level="ERROR", exc_info=True)
        return None

    @exc_handler(on_error_obj_method_name="on_extract_error")
    def extract(self, text_preprocessing_result: BaseTextPreprocessingResult,
                user: User, params: Dict[str, Any] = None) -> Optional[Union[int, float, str, bool, List, Dict]]:
        return self.run(user, text_preprocessing_result, params)


class ElseFiller(ElseAction):
    FIELD_ITEM_KEY = "filler"
    FIELD_ELSE_KEY = "else_filler"

    def on_extract_error(self, text_preprocessing_result, user, params=None):
        log("exc_handler: ElseFiller failed to extract. Return None. MESSAGE: {}.".format(user.message.masked_value),
            user,
            {log_const.KEY_NAME: log_const.HANDLED_EXCEPTION_VALUE}, level="ERROR", exc_info=True)
        return None

    @exc_handler(on_error_obj_method_name="on_extract_error")
    def extract(self, text_preprocessing_result: BaseTextPreprocessingResult,
                user: User, params: Dict[str, Any] = None) -> Optional[Union[int, float, str, bool, List, Dict]]:
        return self.run(user, text_preprocessing_result, params)
