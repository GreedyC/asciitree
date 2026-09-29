from collections import OrderedDict

from asciitree import LeftAligned
from asciitree.drawing import BOX_LIGHT, BoxStyle


def test_default_layout_is_unchanged():
    style = BoxStyle()
    assert style.child_head('label') == ' +-- label'
    assert style.child_tail('line') == ' |  line'
    assert style.last_child_head('label') == ' +-- label'
    assert style.last_child_tail('line') == '    line'


def test_custom_space_in_every_layout_method():
    style = BoxStyle(space=u'\u00a0', indent=2, horiz_len=3, label_space=2)
    assert style.child_head('label') == u'\u00a0\u00a0+---\u00a0\u00a0label'
    assert style.child_tail('line') == u'\u00a0\u00a0|\u00a0\u00a0\u00a0line'
    assert style.last_child_head('label') == u'\u00a0\u00a0+---\u00a0\u00a0label'
    assert style.last_child_tail('line') == u'\u00a0' * 6 + 'line'


def test_nested_tree_preserves_label_spaces():
    tree = {'root label': OrderedDict([
        ('first label', {'leaf label': {}}),
        ('last label', {'last leaf': {}}),
    ])}
    result = LeftAligned(draw=BoxStyle(space=u'\u00a0'))(tree)
    assert result == u'\n'.join([
        'root label',
        u'\u00a0+--\u00a0first label',
        u'\u00a0|\u00a0\u00a0\u00a0+--\u00a0leaf label',
        u'\u00a0+--\u00a0last label',
        u'\u00a0\u00a0\u00a0\u00a0\u00a0+--\u00a0last leaf',
    ])


def test_custom_space_with_unicode_glyphs():
    style = BoxStyle(space=u'\u2003', gfx=BOX_LIGHT)
    assert style.child_head('label') == u'\u2003\u251c\u2500\u2500\u2003label'
    assert style.child_tail('line') == u'\u2003\u2502\u2003\u2003line'
    assert style.last_child_head('label') == u'\u2003\u2514\u2500\u2500\u2003label'
    assert style.last_child_tail('line') == u'\u2003' * 4 + 'line'


def test_zero_padding_counts():
    style = BoxStyle(space=u'\u00a0', indent=0, horiz_len=0, label_space=0)
    assert style.child_head('label') == '+label'
    assert style.child_tail('line') == '|line'
    assert style.last_child_head('label') == '+label'
    assert style.last_child_tail('line') == u'\u00a0line'


def test_custom_space_does_not_change_other_styles():
    custom = BoxStyle(space=u'\u00a0')
    assert custom.child_head('label') != BoxStyle().child_head('label')
    assert BoxStyle().child_head('label') == ' +-- label'


def test_default_preserves_native_string_and_unicode_types():
    for label in ('caf\xc3\xa9', u'caf\xe9'):
        style = BoxStyle()
        for method in (style.child_head, style.child_tail,
                       style.last_child_head, style.last_child_tail):
            assert type(method(label)) is type(label)
            assert method(label).endswith(label)
        result = LeftAligned()({label: {label: {}}})
        assert type(result) is type(label)


def test_custom_space_with_nested_unicode_labels():
    result = LeftAligned(draw=BoxStyle(space=u'\u00a0'))(
        {u'caf\xe9': {u'na\xefve': {u'\u679d': {}}}})
    assert result == u'caf\xe9\n\u00a0+--\u00a0na\xefve\n' + u'\u00a0' * 5 + u'+--\u00a0\u679d'
