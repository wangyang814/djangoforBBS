from django import template

register = template.Library()

class UpperNode(template.Node):
    def __init__(self,rolist):
        self.rolist = rolist
    def render(self, context):
        content = self.rolist.render(context)
        return content.upper()
@register.tag(name='upper')
def upper(parser,token):
    rolist = parser.parse("endupper")
    parser.delete_first_token()
    return UpperNode(rolist)