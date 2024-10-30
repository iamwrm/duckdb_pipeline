import json

class CompactListEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        # Set the indentation level
        self.indent_level = kwargs.pop('indent', 4)
        super().__init__(*args, indent=self.indent_level, **kwargs)

    def encode(self, obj):
        if isinstance(obj, dict):
            items = []
            for key, value in obj.items():
                encoded_key = json.dumps(key)
                encoded_value = self._encode_value(value, self.indent_level)
                items.append(f'{" " * self.indent_level}"{key}": {encoded_value}')
            return '{\n' + ',\n'.join(items) + '\n}'
        else:
            return super().encode(obj)

    def _encode_value(self, value, current_indent):
        if isinstance(value, list):
            # Serialize list in a compact form
            items = ', '.join(self.encode(item) for item in value)
            return f'[{items}]'
        elif isinstance(value, dict):
            # Recursively encode dictionaries
            return self.encode(value)
        else:
            return json.dumps(value)

# Sample data
data = {
    "name": "Alice",
    "age": 30,
    "city": "Wonderland",
    "hobbies": ["reading", "gardening", "chess"],
    "education": {
        "degrees": ["BSc", "MSc"],
        "institutions": ["Wonderland University", "Magic Institute"]
    },
    "projects": [
        {"name": "Project A", "status": "Completed"},
        {"name": "Project B", "status": "Ongoing"}
    ]
}

# Serialize using the custom encoder
pretty_compact_json = json.dumps(
    data,
    cls=CompactListEncoder,
    indent=4
)

print(pretty_compact_json)