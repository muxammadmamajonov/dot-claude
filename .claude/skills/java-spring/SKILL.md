---
name: java-spring
description: >
  Activate when building, reviewing, or debugging Java services with Spring Boot
  (3.x) — beans/DI, JPA/Hibernate, Spring Security, Bean Validation, Actuator,
  virtual threads (Java 21+), and testing with JUnit 5 / Testcontainers. Use
  whenever the work touches Java/Kotlin Spring code, `pom.xml`/`build.gradle`,
  `@RestController`/`@Service`/`@Entity`, or keywords like "spring", "spring boot",
  "hibernate", "jpa" — even if the user just says "Java".
---

# Java + Spring Boot Development

## When to use
- Scaffolding or extending a Spring Boot 3.x service (REST, gRPC, batch, messaging)
- Configuring Spring DI, application context, or Spring component scanning
- Mapping domain objects to the database via Spring Data JPA / Hibernate
- Implementing authentication and authorisation with Spring Security 6
- Adding observability (Actuator, Micrometer, distributed tracing with Micrometer Tracing)
- Writing tests: unit, slice (`@DataJpaTest`, `@WebMvcTest`), and integration with Testcontainers
- Adopting Java 21+ features: virtual threads (Project Loom), records, sealed classes, pattern matching

## Workflow

1. **Scaffold** with [start.spring.io](https://start.spring.io) or `spring initializr` CLI — choose Java 21+, Maven or Gradle (Kotlin DSL preferred), and the minimal starter set needed.
2. **Structure the layers**:
   ```
   src/main/java/com/example/
     api/       ← Controllers / DTOs (presentation)
     service/   ← Business logic (application)
     domain/    ← Entities, value objects, repository interfaces
     infra/     ← JPA repositories, external HTTP clients, config
   ```
   Keep `@Service`, `@Repository`, and `@Controller`/`@RestController` in separate packages — scanning is implicit but the layer contract must be explicit.
3. **Define DTOs / request-response contracts first** using Java records; add `@Valid` Bean Validation annotations (`@NotBlank`, `@Size`, `@Email`, `@Pattern`) and a global `@ControllerAdvice` / `@ExceptionHandler` to return structured RFC 7807 Problem responses.
4. **Map the data model** — see `.claude/skills/data-modeling/SKILL.md`. Annotate `@Entity` classes conservatively: use `FetchType.LAZY` for all associations by default; use `@BatchSize` or `JOIN FETCH` in the repository to avoid N+1.
5. **Secure the application**:
   - Spring Security 6: define a `SecurityFilterChain` bean; prefer `requestMatchers` over `antMatchers`.
   - Stateless REST: JWT via `spring-security-oauth2-resource-server` + `BearerTokenAuthenticationFilter`. Never roll custom JWT parsing.
   - Enable CSRF only for browser-session flows; disable for pure API services.
   - Use method security (`@PreAuthorize("hasRole('ADMIN')")`) for fine-grained control.
6. **Enable Actuator**: expose `health`, `info`, `metrics`, `prometheus` endpoints on a separate management port (`8081`). Hide sensitive endpoints behind `management.endpoint.*.enabled`.
7. **Adopt virtual threads** (Spring Boot 3.2+): set `spring.threads.virtual.enabled=true` — eliminates thread-pool tuning for I/O-heavy services. Do not use virtual threads for CPU-bound compute; use dedicated `@Async` executors with a bounded pool there.
8. **Write tests in layers**:
   - Unit: plain JUnit 5 + Mockito for services/domain logic.
   - Slice: `@WebMvcTest` for controllers; `@DataJpaTest` with an in-memory H2 or Testcontainers Postgres for repositories.
   - Integration: `@SpringBootTest(webEnvironment = RANDOM_PORT)` + Testcontainers for the full stack.
9. **Profile slow queries**: enable `spring.jpa.show-sql=false` in production; use Hibernate statistics (`hibernate.generate_statistics=true`) in dev; log queries >1 s with P6Spy or datasource-proxy.
10. **Audit before deploy** against `.claude/checklists/security.md` and `.claude/checklists/production.md`.

## Standards

### Dependency Injection
- All injectable components are Spring beans — never call `new` on a service class.
- Constructor injection only; `@Autowired` on fields is banned (makes testing hard and hides dependencies).
- Use `@ConfigurationProperties(prefix = "app.feature")` + a record/POJO for typed, validated configuration — never `@Value("${…}")` scattered through business code.
- `@Bean` factory methods go in `@Configuration` classes named `<Feature>Configuration`; do not put `@Bean` in `@Service` classes.

### JPA / Hibernate
- `FetchType.LAZY` for all `@ManyToOne`, `@OneToMany`, `@ManyToMany`. Eager loading is the source of most JPA performance bugs.
- Use `@EntityGraph` or `JOIN FETCH` in the repository method that needs the data — co-locate the fetch strategy with the query.
- Prefer Spring Data derived queries or `@Query` JPQL for simple reads; use `JdbcTemplate` or `jOOQ` for complex reporting queries — do not abuse JPQL for 10-join analytics.
- Never expose JPA entities as REST response bodies — always map to DTOs. This prevents lazy-initialisation serialisation failures and over-exposure.
- `@Transactional(readOnly = true)` on query-only service methods — this sets the Hibernate flush mode to NEVER and allows read-only JDBC optimisations.
- Migrations: use **Flyway** (preferred) or Liquibase, never `ddl-auto=update` in any environment beyond local dev.

### Validation
- Validate at the API boundary with `@Valid` on `@RequestBody` and method parameters.
- Custom constraints: implement `ConstraintValidator<A, T>` — do not hand-roll if-else chains in service code.
- Return 400 with a structured error body listing all violations; never 500 for validation failures.

### Security
- Password storage: `BCryptPasswordEncoder` (cost ≥ 12) or `Argon2PasswordEncoder` — never MD5, SHA-1, or plain text.
- Secrets from environment variables or a secret manager (AWS Secrets Manager, Vault) — never in `application.yml` committed to VCS.
- HTTP Security headers: add `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy` via `headers()` in `SecurityFilterChain`.

### Do not
- Do not use `spring.jpa.hibernate.ddl-auto=update` in staging or production.
- Do not catch `Exception` generically and swallow it; catch specific exceptions and convert to typed domain errors.
- Do not use `@SpringBootTest` for everything — slice tests are 10x faster.
- Do not expose `env`, `beans`, or `httptrace` Actuator endpoints publicly.
- Do not block virtual threads with `synchronized` on contested monitors — use `ReentrantLock` instead (virtual-thread pinning).

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| N+1 queries from `FetchType.LAZY` in a loop | Use `@EntityGraph` or `JOIN FETCH` in the repository for that specific use case |
| `LazyInitializationException` outside a transaction | Move the fetch inside the `@Transactional` boundary or use a DTO projection |
| `@Transactional` on private methods | Spring AOP proxies only intercept public methods; move logic to a public method or use `AspectJ` weaving |
| Fat controllers with business logic | Business logic lives in `@Service`; controllers only parse, delegate, and map responses |
| `application.properties` with plain-text passwords | Use `spring.config.import=optional:configserver:` or environment variable references |
| Circular bean dependencies | Introduce an interface, event, or factory to break the cycle; do NOT use `@Lazy` as a workaround |
| Missing `@Transactional` on multi-step mutations | Any operation that writes to more than one table must be wrapped in a transaction |

## Output format

- New service: directory layout with `pom.xml` / `build.gradle.kts` excerpt, `application.yml` skeleton, and `SecurityFilterChain` bean.
- Entity + repository: annotated `@Entity` class, Spring Data `JpaRepository` interface, and a Flyway migration SQL file.
- Test: JUnit 5 class using `@WebMvcTest` or `@DataJpaTest` with MockMvc assertions and Testcontainers setup.
- Security config: complete `SecurityFilterChain` `@Bean` with JWT resource-server configuration.

Output artifacts go to `docs/specs/` (architecture decisions) or alongside source files (test classes, migration SQL).

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
