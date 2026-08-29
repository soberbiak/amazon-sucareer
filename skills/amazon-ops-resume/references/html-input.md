# HTML builder input

The builder expects UTF-8 JSON:

```json
{
  "fictional": true,
  "mode": "experienced",
  "layout_density": "standard",
  "name": "Example Name",
  "target_role": "Amazon Operations",
  "contact": ["City", "email@example.test"],
  "summary": ["First supported summary line."],
  "skills": ["Portfolio diagnosis", "Advertising governance"],
  "sections": [
    {
      "title": "Work Experience",
      "items": [
        {
          "heading": "Fictional Company · Role",
          "meta": "2024.01–2025.01 · City",
          "subheading": "Optional scope statement",
          "bullets": ["Evidence-backed bullet"]
        }
      ]
    }
  ]
}
```

Required fields are `mode`, `name`, `target_role`, `contact`, `summary`, `skills`, and `sections`. `mode` must be `campus` or `experienced`. `layout_density` is optional: `compact` prioritizes one page, `standard` is the default, and `comfortable` increases major-section spacing. The builder escapes all input text and does not accept raw HTML.
