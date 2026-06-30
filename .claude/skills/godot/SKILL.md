---
name: godot
description: >
  Activate when building, debugging, or architecting games or interactive apps
  with Godot Engine 3 or 4 — GDScript, C#, scene composition, signals, export
  pipeline, and performance practices. Use whenever the work touches Godot,
  `.gd`/`.tscn`/`project.godot` files, nodes/scenes/signals, or keywords like
  "godot", "gdscript", "scene tree" — even if the user just says "my game".
---

# Godot Engine Development

## When to use
- Writing or reviewing GDScript or C# game scripts
- Designing scene trees, node hierarchies, and resource types
- Implementing signals, groups, and the Godot event model
- Profiling and fixing draw-call, physics, or script bottlenecks
- Configuring export templates and platform-specific settings
- Integrating GDExtension (native C/C++) plugins

## Workflow

1. **Confirm Godot version** — Godot 3 (GDScript 1, `KinematicBody`) vs Godot 4 (GDScript 2, `CharacterBody3D`, Vulkan, `@tool` decorators, typed arrays). API differs substantially.
2. **Model the scene tree first** — sketch the node hierarchy on paper or in comments before scripting. Child nodes should not call methods on parents; use signals upward.
3. **Choose the right node base**:
   - Static world geometry → `StaticBody3D` + `MeshInstance3D`.
   - Player / NPC → `CharacterBody3D` (Godot 4) or `KinematicBody` (Godot 3) with `move_and_slide`.
   - UI → `Control` nodes inside a `CanvasLayer`.
   - Data-only shared state → `Resource` subclass (saved as `.tres`).
4. **Script the node** — attach a script; use `class_name` for autocompletion and type hints. Type all variables: `var speed: float = 5.0`.
5. **Emit signals upward, call methods downward** — parent can call `$Child.do_thing()`; child must emit a signal that parent connects to. Never `get_parent().something()` in child scripts.
6. **Use `_ready`, `_process`, `_physics_process` correctly**:
   - `_ready`: one-time init after node enters the scene tree.
   - `_physics_process(delta)`: physics-safe movement; use `move_and_slide` here.
   - `_process(delta)`: per-frame logic (input, animation state).
7. **Test in-editor** with the debugger and Profiler panel open. Check Monitor → Physics/Process for budget.
8. **Optimize**:
   - Reduce draw calls: use `MultiMeshInstance3D` for repeated objects.
   - Disable `_process` when node is off-screen via `set_process(false)`.
   - Pool nodes with `Queue` autoload instead of `queue_free` + `instantiate` every frame.
9. **Export**: Project → Export → add template for each platform. Set VRAM compression, PCK embed, and verify export template version matches editor version.
10. **Audit** using .claude/checklists/performance.md and .claude/checklists/qa.md.

## Standards

### GDScript (Godot 4)
- Use static typing everywhere: `func move(direction: Vector2) -> void:`.
- Prefer `@export var speed: float = 5.0` over bare `var` for designer-editable fields.
- Use `@onready var _label: Label = $UI/Label` (GD4) instead of `onready` (GD3).
- Group related signals at the top of the file with `signal health_changed(new_health: int)`.
- Keep `_process` bodies under 0.5 ms; offload heavy computation to `Thread` or `WorkerThreadPool`.

### C# (GodotSharp)
- Use `[Export]` attribute for inspector properties.
- Connect signals via `SignalName` constants (`EmitSignal(SignalName.HealthChanged, newHealth)`).
- Dispose `Timer`, `Tween`, and `AudioStreamPlayer` nodes explicitly or let the scene tree own them.
- Async/await: use `ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame)` for Godot-aware awaiting.

### Scene and resource hygiene
- One scene per logical game object; nest prefab-like scenes with inherited scenes for variants.
- Store shared data as `Resource` files (`.tres`) not as singleton state.
- Autoloads (singletons) only for truly global services: `GameState`, `AudioBus`, `SaveManager`.

### Do not
- Do not use `get_node("/root/GameState")` absolute paths — use typed autoloads or dependency injection via `@export`.
- Do not call `get_children()` every frame — cache the reference in `_ready`.
- Do not block the main thread with `File.open` / HTTP requests — use `FileAccess` async or `HTTPRequest` node.
- Do not mix GDScript 1 and GDScript 2 idioms in Godot 4 projects — they are not compatible.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| Modifying nodes in `_init` before they're in the scene tree | Move to `_ready`; `_init` runs before tree entry. |
| Connecting signal to a freed node | Use `is_instance_valid(target)` check or disconnect in `_exit_tree`. |
| Using `yield` (GD3) syntax in Godot 4 | Replace with `await`. |
| Physics jitter from moving objects in `_process` | Always move physics bodies in `_physics_process`. |
| Giant monolithic `GameManager` autoload | Split into focused singletons: `SaveManager`, `SceneLoader`, `EventBus`. |
| Exporting without matching template version | Download templates from Project → Install Export Templates matching editor version. |

## Output format

- New script: `.gd` file with `class_name`, typed properties, signals, and lifecycle methods in order.
- Scene layout: text tree showing node types and nesting.
- Signal diagram: emitter → signal name → receiver for multi-node interactions.
- Performance fix: before/after profiler reading + one-line change description.

## Related checklists
- .claude/checklists/performance.md
- .claude/checklists/qa.md
- .claude/checklists/accessibility.md

## Related agents
- .claude/agents/core/orchestrator.md
- .claude/agents/engineering/devops-engineer.md
