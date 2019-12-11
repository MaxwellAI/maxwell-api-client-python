from marshmallow import fields, post_load, Schema

from maxwell.model.base import Model


class CallToActionSchema(Schema):
    type = fields.Str()
    title = fields.Str()
    payload = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)
    webview_height_ratio = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return CallToAction(**data)


class CallToAction(Model):
    TYPES = ("postback", "web_url")
    WEBVIEW_HEIGHT_RATIOS = ("full", "compact", "tall")

    def __init__(
        self, type, title, payload=None, url=None, webview_height_ratio=None
    ):
        assert type in self.TYPES
        assert (
            webview_height_ratio is None
            or webview_height_ratio in self.WEBVIEW_HEIGHT_RATIOS
        )
        self.type = type
        self.title = title
        self.payload = payload
        self.url = url
        self.webview_height_ratio = webview_height_ratio
