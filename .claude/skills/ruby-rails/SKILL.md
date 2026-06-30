---
name: ruby-rails
description: >
  Activate when building, reviewing, or debugging Ruby on Rails 7+ applications —
  ActiveRecord, strong parameters, Action Mailer, Sidekiq background jobs, Hotwire
  (Turbo + Stimulus), security defaults (CSP, CSRF, mass-assignment), and RSpec /
  Minitest testing. Use whenever the work touches Ruby/Rails code, `Gemfile`,
  `bin/rails`, models/controllers/migrations, or keywords like "rails", "activerecord",
  "sidekiq", "hotwire" — even if the user just says "Ruby".
---

# Ruby on Rails Development

## When to use
- Scaffolding or extending a Rails 7+ application (full-stack, API-only, or hybrid)
- Designing ActiveRecord models, associations, validations, and callbacks
- Writing database migrations and managing schema changes
- Implementing background jobs with Sidekiq and ActiveJob
- Building reactive UIs with Hotwire (Turbo Frames, Turbo Streams, Stimulus)
- Hardening Rails security defaults (CSRF, CSP, mass-assignment, host authorisation)
- Testing with RSpec + FactoryBot or Minitest

## Workflow

1. **Scaffold** with `rails new my-app` (full stack) or `rails new my-api --api` (API-only). For API-only apps add `--skip-asset-pipeline --skip-javascript`. Use Ruby 3.3+ and Rails 7.2+.
2. **Structure the application**:
   ```
   app/
     controllers/    ← Thin: permit params, call service/command, respond
     models/         ← ActiveRecord: associations, validations, scopes
     services/       ← Business logic POROs (Plain Old Ruby Objects)
     jobs/           ← ActiveJob / Sidekiq jobs
     views/          ← ERB templates + Turbo partials
     components/     ← ViewComponent for complex UI components (optional)
   ```
   Keep controllers thin — one controller action should: permit params → call one service object → render/redirect.
3. **Define the data model** — see `.claude/skills/data-modeling/SKILL.md`. Generate migrations with `rails generate migration`. Follow the `YYYYMMDDHHMMSS_verb_noun_on_table.rb` naming convention.
4. **ActiveRecord models**:
   - Declare `belongs_to`, `has_many`, `has_one`, `has_and_belongs_to_many` relationships explicitly.
   - Add database-level constraints AND ActiveRecord validations — they are complementary, not redundant.
   - Use named scopes (`scope :active, -> { where(status: 'active') }`) for reusable query fragments.
   - Callbacks (`before_save`, `after_create`) only for concerns tightly coupled to persistence. Side effects (emails, jobs) belong in service objects, not callbacks.
5. **Strong parameters**: permit only what is needed in `params.require(:model).permit(:field1, :field2)`. Never `params.permit!`. Extract a private `model_params` method in the controller.
6. **Authenticate and authorise**:
   - Authentication: `has_secure_password` + `authenticate` for simple apps; Devise for full auth with email confirmation, 2FA, etc.
   - Authorisation: Pundit (policy objects, clean `authorize @model`) or CanCanCan (ability-based). Never inline `if current_user.admin?` in views.
   - API tokens: Devise Token Auth or JWT via `jwt` gem with a server-side allowlist for revocation.
7. **Background jobs** with Sidekiq + ActiveJob:
   - Inherit from `ApplicationJob < ActiveJob::Base`; set `queue_as :default` or `:critical`.
   - Jobs must be idempotent — they may run more than once (retry on failure).
   - Pass only primitive arguments (IDs, strings) — not ActiveRecord objects (they serialise and may be stale).
   - Set `sidekiq_options retry: 5, backtrace: 10` on the job class for tuning.
   - Use `Sidekiq::Testing.fake!` in tests; assert with `assert_enqueued_with`.
8. **Hotwire (Turbo + Stimulus)**:
   - Turbo Frames (`<turbo-frame id="…">`) for lazy-loading and partial page updates.
   - Turbo Streams for broadcasting real-time updates via `ActionCable` or from controller responses.
   - Stimulus controllers for JavaScript behaviour scoped to a DOM element — never global jQuery-style selectors.
   - Avoid full-page redirects where a Turbo Stream response keeps the user in context.
9. **Security defaults**:
   - `protect_from_forgery` is on by default for HTML responses — never disable it.
   - Content Security Policy: configure in `config/initializers/content_security_policy.rb` — tighten `script-src`, `style-src`, `connect-src`.
   - `config.hosts` (Rails 6.1+): restrict to known hostnames in production; `allow_all_hosts` is development-only.
   - Force SSL: `config.force_ssl = true` in `production.rb`.
   - Sensitive attributes: `has_secure_password` manages the digest; never store plain passwords.
10. **Write tests**:
    - RSpec: model specs (validations, scopes), request specs (API endpoints), system specs (Capybara for full browser flow).
    - FactoryBot for test data — define factories, not fixtures, for flexibility.
    - `database_cleaner` or `use_transactional_fixtures: true` to reset state between tests.
    - VCR (`vcr` gem) to record and replay external HTTP interactions in tests.
11. **Audit** against `.claude/checklists/security.md` and `.claude/checklists/production.md`.

## Standards

### ActiveRecord
- `belongs_to` is required by default (Rails 5+) — add `optional: true` only when the FK is genuinely nullable.
- Add `counter_cache: true` for `has_many` counts that are queried frequently.
- Avoid `where("column = '#{value}'")` — always use hash syntax or parameterised strings: `where(column: value)` or `where("column = ?", value)`.
- Use `find_each` or `in_batches` for bulk processing — never `.all` on a potentially large table.
- Transactions: `ActiveRecord::Base.transaction { ... }` for multi-model writes.

### Migrations
- Migrations are immutable once run on shared environments — create new migrations, never edit committed ones.
- Use `add_index` with `algorithm: :concurrently` on PostgreSQL for zero-lock index creation; note this requires running the migration outside a transaction (`disable_ddl_transaction!`).
- Column removals: two-step — first deploy ignoring the column, then drop it in the next release (avoids `ActiveRecord::UnknownAttributeError`).
- `null: false` and `default:` constraints in migrations for required columns.

### Services / POROs
- One public method (typically `call`), one responsibility.
- Accept dependencies via constructor injection — makes testing with mocks straightforward.
- Raise a typed error (`MyService::Error < StandardError`) instead of returning `false` for failure.

### Do not
- Do not put business logic in controllers or views.
- Do not use `update_column` (skips validations and callbacks) unless you explicitly need that and document why.
- Do not use `Model.all` without a `limit` in application code paths that could return unbounded rows.
- Do not enable `config.allow_all_hosts` in staging or production.
- Do not use synchronous HTTP calls in a controller action without a timeout; move to a background job.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| N+1 queries from missing `includes` | Use `includes(:association)` or `eager_load`; detect with `bullet` gem |
| Callback side-effects (emails, jobs) in ActiveRecord | Move to service objects; trigger from controller after successful save |
| `params.permit!` allowing arbitrary mass assignment | Explicitly whitelist each attribute in `permit(...)` |
| Memory bloat from `Post.all` on large tables | Use `find_each(batch_size: 500)` or `lazy` enumerators |
| Synchronous Sidekiq tests asserting on real queue | Use `Sidekiq::Testing.fake!` in spec helper; `Sidekiq::Testing.drain_all` to process inline |
| Missing database-level uniqueness constraint | `add_index :users, :email, unique: true` plus `validates :email, uniqueness: true` |
| String interpolation in `where` clauses | Always use `where("name = ?", value)` or hash syntax to prevent SQL injection |

## Output format

- New resource: migration, model with validations and associations, controller with strong params, RSpec request spec.
- Service object: PORO with `call` method, constructor dependencies, typed error class, and RSpec unit spec.
- Background job: ActiveJob class, Sidekiq options, idempotency check, and `assert_enqueued_with` test.
- Hotwire interaction: controller action returning `turbo_stream` format, partial template, and Stimulus controller.

Output artifacts go to `docs/specs/` for design decisions; code files in `app/` tree.

## Related checklists
- .claude/checklists/security.md
- .claude/checklists/performance.md
- .claude/checklists/qa.md
- .claude/checklists/production.md

## Related agents
- .claude/agents/core/solution-architect.md
- .claude/agents/engineering/backend-engineer.md
- .claude/agents/engineering/database-architect.md
- .claude/agents/quality/security-auditor.md
