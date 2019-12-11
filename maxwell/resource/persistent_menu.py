from marshmallow import fields, post_load, Schema

from maxwell.model.base import Model
from maxwell.model.call_to_action import CallToAction, CallToActionSchema
from maxwell.resource.base import Resource


class LocalizedPersistentMenu(Model):
    def __init__(
        self,
        call_to_actions=None,
        locale="default",
        composer_input_disabled=False,
    ):
        call_to_actions = call_to_actions or []
        assert all([isinstance(c, CallToAction) for c in call_to_actions])
        self.call_to_actions = call_to_actions
        self.locale = locale
        self.composer_input_disabled = composer_input_disabled


class LocalizedPersistentMenuSchema(Schema):
    call_to_actions = fields.Nested(CallToActionSchema, many=True)
    locale = fields.String(default="default")
    composer_input_disabled = fields.Boolean(default=False)

    @post_load
    def make_object(self, data, **kwargs):
        return PersistentMenu(**data)


class PersistentMenuSchema(Schema):
    persistent_menu = fields.Nested(LocalizedPersistentMenuSchema, many=True)


class PersistentMenu(Resource):
    _path = "persistent-menus"
    _slug = "persistent_menu"

    def __init__(
        self, persistent_menu=None, client=None, parent=None, **kwargs
    ):
        super().__init__(client, parent)
        persistent_menu = persistent_menu or []
        assert all([isinstance(p, PersistentMenu) for p in persistent_menu])
        self.persistent_menu = persistent_menu

    def get(self):
        persistent_menu = LocalizedPersistentMenuSchema(many=True).load(
            self._request()[self._slug] or []
        )
        return PersistentMenu(
            client=self._client,
            parent=self._parent,
            persistent_menu=persistent_menu,
        )

    def update(self, persistent_menu):
        assert all(
            [
                isinstance(p, PersistentMenu)
                for p in persistent_menu.persistent_menu
            ]
        )
        data = PersistentMenuSchema().dump(persistent_menu)
        return self._request(method="put", data=data)

    def delete(self):
        return self._request(method="delete")
