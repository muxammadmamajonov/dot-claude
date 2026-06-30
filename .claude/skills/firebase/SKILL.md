---
name: firebase
description: >
  Activate when the project uses Firebase: Firestore, Firebase Auth,
  Firebase Storage, Cloud Functions for Firebase, Firebase Hosting,
  Firebase Realtime Database, or Remote Config. Also activate when debugging
  Firestore security rules, designing collection schemas, or setting up
  Firebase Emulators for local development.
---

# Firebase Skill

## When to use

- Architecting Firestore collection/subcollection structure and indexes
- Writing and testing Firestore Security Rules
- Implementing Firebase Auth (email/password, OAuth, custom tokens, custom claims)
- Writing Cloud Functions for Firebase (v1 HTTP, callable, background triggers)
- Configuring Firebase Hosting with rewrite rules to Cloud Functions or Cloud Run
- Setting up the Firebase Emulator Suite for local development and CI
- Diagnosing quota/billing issues, missing indexes, or security-rule denial errors

---

## Workflow

1. **Design the data model before writing code** — Firestore is schemaless but reads are charged per document. Denormalize data intentionally: embed sub-objects that are always read together; use subcollections for unbounded lists.
2. **Initialize the project**: `firebase init` → select Firestore, Functions, Hosting, Emulators. Commit `.firebaserc` and `firebase.json`; gitignore `functions/node_modules`.
3. **Write Security Rules early** — create `firestore.rules` with deny-all as the default, then open exactly what each user role needs. Mirror the same pattern for `storage.rules`.
4. **Test rules with the Emulator** — run `firebase emulators:start` and point the SDK at `localhost:8080` (Firestore) / `localhost:9099` (Auth). Use `@firebase/rules-unit-testing` for automated rule tests.
5. **Add composite indexes via `firestore.indexes.json`** — never create them only in the console; indexes defined in the file are reproducible across environments.
6. **Cloud Functions**: keep each function focused on a single trigger. Use `onCall` for client-invoked logic (handles Auth context automatically). Use `onDocumentWritten`/`onDocumentCreated` for server-side side effects. Avoid chaining background triggers (trigger → function → write → trigger) as this creates infinite loops.
7. **Deploy incrementally**: `firebase deploy --only firestore:rules`, then `--only functions`, then `--only hosting` to limit blast radius.
8. **Before production**: run `firebase firestore:indexes` to confirm indexes are deployed; check the Firebase console → Usage tab for quota headroom.

---

## Standards

### Do
- Use `FieldValue.serverTimestamp()` for `createdAt`/`updatedAt` — never trust client-supplied timestamps.
- Keep Security Rules DRY by extracting helper functions: `function isOwner(uid) { return request.auth.uid == uid; }`.
- Version Cloud Functions explicitly in `package.json` and pin `firebase-admin` and `firebase-functions`.
- Use `admin.auth().verifyIdToken()` in HTTP functions to authenticate callers — never trust a UID passed in the request body.
- Set `region` explicitly on functions deployed to non-`us-central1` regions so client SDKs can connect.
- Use environment config (`firebase functions:config:set`) or Secret Manager (v2 functions) for secrets — never hardcode.

### Do not
- Do not use `allow read, write: if true;` in Security Rules even temporarily in a shared repo.
- Do not store more than ~1 MB of data in a single Firestore document (hard limit is 1 MiB; practical limit is much lower to avoid slow reads).
- Do not use Firestore as a queue — use Cloud Tasks or Pub/Sub for background job delivery.
- Do not run Firestore queries without an equality/range filter on an indexed field; collection-group queries with no filter cause full-collection scans.
- Do not mix client SDK and admin SDK in the same runtime context.
- Do not use `onSnapshot` listeners in Cloud Functions (they run serverless and have no persistent connection).

---

## Common mistakes to avoid

| Mistake | Consequence | Fix |
|---|---|---|
| Missing composite index on a multi-field query | Runtime error thrown to client | Add to `firestore.indexes.json`; deploy before the query goes live |
| Background-trigger infinite loop | Runaway invocations → billing shock | Guard with a state flag: check if the document field already has the expected value before writing |
| Returning sensitive fields in Security Rules `get()` calls | Data exfiltration via rule side-channel | Rules can call `get()` but the fetched data is only visible to the rule engine, not the client — still, limit `get()` usage to avoid extra reads |
| Using `collection.get()` (fetch all docs) in a Cloud Function | Memory exhaustion for large collections | Paginate with `startAfter` or use a Firestore aggregation query |
| Deploying functions without setting a minimum instance count for latency-sensitive paths | Cold-start delays of 2–5 s | Set `minInstances: 1` on functions behind user-facing APIs |
| Not initializing Firebase Admin with `cert()` in non-Google Cloud environments | `GOOGLE_APPLICATION_CREDENTIALS` missing → auth failure | Pass `admin.initializeApp({ credential: admin.credential.cert(serviceAccount) })` |

---

## Output format

```
firebase.json           — hosting rewrites, function config
firestore.rules         — Security Rules
firestore.indexes.json  — composite indexes
storage.rules           — Storage Security Rules
functions/
  src/
    index.ts            — function exports
    auth/               — auth trigger handlers
    http/               — HTTP/callable handlers
    firestore/          — document trigger handlers
  package.json
.firebaserc             — project aliases (default, staging, prod)
```

Cloud Function pattern:
```ts
export const createUserProfile = onCall({ region: "us-central1" }, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Login required");
  const uid = request.auth.uid;
  await admin.firestore().doc(`profiles/${uid}`).set({ createdAt: FieldValue.serverTimestamp() });
  return { success: true };
});
```

---

## Related checklists
- `.claude/checklists/security.md`
- `.claude/checklists/database.md`
- `.claude/checklists/launch.md`

## Related agents
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/core/system-analyst.md`
