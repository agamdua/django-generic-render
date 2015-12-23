# -*- coding: utf-8 -*-

import inspect

from django.views.generic.list import ListView


def apply_config(view_object, object_list):
    """
    Example config for model Candy:

        render_config = [
            {'name': {'column_name': 'Candy Name', css_class_extra: 'highlight'},  # noqa
            {'price': {'column_name': 'Price', 'prepend_value': '$'}},
            {'url': {'column_name': 'Buy', 'anchor': True }}

    """
    config = view_object.Meta.render_config

    render_attrs = {
        'field_names': config.keys(),  # assumed to be in the order required
        'column_attrs': [
            type(field_name, (), **column_config)
            for field_name, column_config in config.items()
        ]
    }

    object_list.Render = type('Render', (), **render_attrs)

    return object_list


def get_object_list_context_data(self, original_get_context_data, *args, **kwargs):  # noqa
    """
    This method to be used when self.object_list is present

    TODO: take care of the object_list alias
    """
    context_data = self.original_get_context_data(*args, **kwargs)

    object_list = context_data['object_list']
    object_list = apply_config(self, object_list)
    context_data['object_list'] = object_list

    return context_data


def GenericRender(cls):
    klass = type(
        'New' + cls.__name__, cls.__bases__, cls.__dict__
    )

    if inspect.issubclass(klass, ListView):
        klass.original_get_context_data = klass.get_context_data
        klass.get_context_data = klass.get_object_list_context_data

        return klass
