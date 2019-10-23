# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: {{ ', '.join(description.files) }}
# plugin: python-betterproto
from dataclasses import dataclass
{% if description.typing_imports %}
from typing import {% for i in description.typing_imports %}{{ i }}{% if not loop.last %}, {% endif %}{% endfor %}

{% endif %}

import betterproto
{% if description.services %}
import grpclib
{% endif %}
{% for i in description.imports %}

{{ i }}
{% endfor %}


{% if description.enums %}{% for enum in description.enums %}
class {{ enum.name }}(betterproto.Enum):
    {% if enum.comment %}
{{ enum.comment }}

    {% endif %}
    {% for entry in enum.entries %}
        {% if entry.comment %}
{{ entry.comment }}
        {% endif %}
    {{ entry.name }} = {{ entry.value }}
    {% endfor %}


{% endfor %}
{% endif %}
{% for message in description.messages %}
@dataclass
class {{ message.name }}(betterproto.Message):
    {% if message.comment %}
{{ message.comment }}

    {% endif %}
    {% for field in message.properties %}
        {% if field.comment %}
{{ field.comment }}
        {% endif %}
    {{ field.name }}: {{ field.type }} = betterproto.{{ field.field_type }}_field({{ field.number }}{% if field.field_type == 'map'%}, betterproto.{{ field.map_types[0] }}, betterproto.{{ field.map_types[1] }}{% endif %}{% if field.one_of %}, group="{{ field.one_of }}"{% endif %})
    {% endfor %}
    {% if not message.properties %}
    pass
    {% endif %}


{% endfor %}
{% for service in description.services %}
class {{ service.name }}Stub(betterproto.ServiceStub):
    {% if service.comment %}
{{ service.comment }}

    {% endif %}
    {% for method in service.methods %}
    async def {{ method.py_name }}(self{% if method.input_message and method.input_message.properties %}, *, {% for field in method.input_message.properties %}{{ field.name }}: {% if field.zero == "None" %}Optional[{{ field.type }}]{% else %}{{ field.type }}{% endif %} = {{ field.zero }}{% if not loop.last %}, {% endif %}{% endfor %}{% endif %}) -> {% if method.server_streaming %}AsyncGenerator[{{ method.output }}, None]{% else %}{{ method.output }}{% endif %}:
        {% if method.comment %}
{{ method.comment }}

        {% endif %}
        request = {{ method.input }}()
        {% for field in method.input_message.properties %}
            {% if field.field_type == 'message' %}
        if {{ field.name }} is not None:
            request.{{ field.name }} = {{ field.name }}
            {% else %}
        request.{{ field.name }} = {{ field.name }}
            {% endif %}
        {% endfor %}

        {% if method.server_streaming %}
        async for response in self._unary_stream(
            "{{ method.route }}",
            {{ method.input }},
            {{ method.output }},
            request,
        ):
            yield response
        {% else %}
        return await self._unary_unary(
            "{{ method.route }}",
            {{ method.input }},
            {{ method.output }},
            request,
        )
        {% endif %}

    {% endfor %}
{% endfor %}
