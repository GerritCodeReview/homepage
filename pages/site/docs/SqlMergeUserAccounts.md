---
title: "SQL Merge User Accounts"
permalink: sqlmergeuseraccounts.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

## Introduction

Sometimes users wind up with two accounts on a Gerrit server, this is especially
common with OpenID installations when the user forgets which OpenID provider he
had used, and opens yet another account with a different OpenID identity... but
the site administrator knows they are the same person.

Unfortunately this has happened often enough on review.source.android.com that
I've developed a set of PostgreSQL scripts to handle merging the accounts.

The first script, load\_merge.sql, creates a temporary table called "links"
which contains a mapping of source account\_id to destination account\_id. This
mapping tries to map the most recently created account for a user to the oldest
account for the same user, by comparing email addresses and registration dates.
Administrators can (and probably should) edit this temporary table before
running the second script. The second script, merge\_accounts.sql, performs the
merge by updating all records in the database in a transaction, but does not
commit it at the end. This allows the administrator to double check any records
by query before committing the merge result for good.

## load\_merge.sql

```
CREATE TEMP TABLE links
(from_id INT NOT NULL
,to_id INT NOT NULL);

DELETE FROM links;

INSERT INTO links (from_id, to_id)
SELECT
 f.account_id
,t.account_id
FROM
 accounts f
,accounts t
WHERE
     f.preferred_email is not null
 AND t.preferred_email is not null
 AND f.account_id <> t.account_id
 AND f.preferred_email = t.preferred_email
 AND f.registered_on > t.registered_on
 AND NOT EXISTS (SELECT 1 FROM links l
                 WHERE l.from_id = f.account_id
                   AND l.to_id = t.account_id);

INSERT INTO links (from_id, to_id)
SELECT DISTINCT
 f.account_id
,t.account_id
FROM
 account_external_ids e_t
,account_external_ids e_f
,accounts f
,accounts t
WHERE
     e_t.external_id = 'Google Account ' || e_f.email_address
 AND e_f.account_id <> e_t.account_id
 AND e_f.account_id = f.account_id
 AND e_t.account_id = t.account_id
 AND f.registered_on > t.registered_on
 AND NOT EXISTS (SELECT 1 FROM links l
                 WHERE l.from_id = f.account_id
                   AND l.to_id = t.account_id);

SELECT
 l.from_id
,l.to_id
,f.registered_on
,t.registered_on
,t.preferred_email
FROM
 links l
,accounts f
,accounts t
WHERE
    f.account_id = l.from_id
AND t.account_id = l.to_id
ORDER BY t.preferred_email;
```

## merge\_accounts.sql

```
DROP TABLE to_del;
CREATE TEMP TABLE to_del (old_id INT);

CREATE TEMP TABLE tmp_ids
(email_address VARCHAR(255)
,account_id INT NOT NULL
,from_account_id INT NOT NULL
,external_id VARCHAR(255) NOT NULL
);

BEGIN TRANSACTION;

DELETE FROM tmp_ids;
INSERT INTO tmp_ids
(account_id
,from_account_id
,email_address
,external_id)
SELECT
 l.to_id
,l.from_id
,e.email_address
,e.external_id
FROM links l, account_external_ids e
WHERE e.account_id = l.from_id
AND NOT EXISTS (SELECT 1 FROM account_external_ids q
  WHERE q.account_id = l.to_id
  AND q.external_id = e.external_id);

DELETE FROM account_external_ids
WHERE EXISTS (SELECT 1 FROM tmp_ids t
  WHERE account_external_ids.external_id = t.external_id
  AND account_external_ids.account_id = t.from_account_id);

INSERT INTO account_external_ids
(account_id
,email_address
,external_id)
SELECT
 account_id
,email_address
,external_id
FROM tmp_ids;

INSERT INTO account_ssh_keys
(ssh_public_key
,valid
,account_id
,seq)
SELECT
 k.ssh_public_key
,k.valid
,l.to_id
,100 + k.seq
FROM links l, account_ssh_keys k
WHERE k.account_id = l.from_id
AND NOT EXISTS (SELECT 1 FROM account_ssh_keys p
  WHERE p.account_id = l.to_id
    AND p.ssh_public_key = k.ssh_public_key);

INSERT INTO starred_changes
(account_id, change_id)
SELECT l.to_id, s.change_id
FROM links l, starred_changes s
WHERE l.from_id IS NOT NULL
  AND l.to_id IS NOT NULL
  AND s.account_id = l.from_id
  AND NOT EXISTS (SELECT 1 FROM starred_changes e
                  WHERE e.account_id = l.to_id
                  AND e.change_id = s.change_id);

INSERT INTO account_project_watches
(account_id, project_name)
SELECT l.to_id, s.project_name
FROM links l, account_project_watches s
WHERE l.from_id IS NOT NULL
  AND l.to_id IS NOT NULL
  AND s.account_id = l.from_id
  AND NOT EXISTS (SELECT 1 FROM account_project_watches e
                  WHERE e.account_id = l.to_id
                  AND e.project_name = s.project_name);

INSERT INTO account_group_members
(account_id, group_id)
SELECT l.to_id, s.group_id
FROM links l, account_group_members s
WHERE l.from_id IS NOT NULL
  AND l.to_id IS NOT NULL
  AND s.account_id = l.from_id
  AND NOT EXISTS (SELECT 1 FROM account_group_members e
                  WHERE e.account_id = l.to_id
                  AND e.group_id = s.group_id);

UPDATE changes
SET owner_account_id = (SELECT l.to_id
                        FROM links l
                        WHERE l.from_id = owner_account_id)
WHERE EXISTS (SELECT 1 FROM links l
              WHERE l.to_id IS NOT NULL
                AND l.from_id IS NOT NULL
                AND l.from_id = owner_account_id);

UPDATE patch_sets
SET uploader_account_id = (SELECT l.to_id
                           FROM links l
                           WHERE l.from_id = uploader_account_id)
WHERE EXISTS (SELECT 1 FROM links l
              WHERE l.to_id IS NOT NULL
                AND l.from_id IS NOT NULL
                AND l.from_id = uploader_account_id);

UPDATE patch_set_approvals
SET account_id = (SELECT l.to_id
                  FROM links l
                  WHERE l.from_id = account_id)
WHERE EXISTS (SELECT 1 FROM links l
              WHERE l.to_id IS NOT NULL
                AND l.from_id IS NOT NULL
                AND l.from_id = account_id)
 AND NOT EXISTS (SELECT 1 FROM patch_set_approvals e, links l
                 WHERE e.change_id = patch_set_approvals.change_id
                   AND e.patch_set_id = patch_set_approvals.patch_set_id
                   AND e.account_id = l.to_id
                   AND e.category_id = patch_set_approvals.category_id
                   AND l.from_id = patch_set_approvals.account_id);

UPDATE change_messages
SET author_id = (SELECT l.to_id
                 FROM links l
                 WHERE l.from_id = author_id)
WHERE EXISTS (SELECT 1 FROM links l
              WHERE l.to_id IS NOT NULL
                AND l.from_id IS NOT NULL
                AND l.from_id = author_id);

UPDATE patch_comments
SET author_id = (SELECT l.to_id
                 FROM links l
                 WHERE l.from_id = author_id)
WHERE EXISTS (SELECT 1 FROM links l
              WHERE l.to_id IS NOT NULL
                AND l.from_id IS NOT NULL
                AND l.from_id = author_id);


-- Destroy the from account
--
INSERT INTO to_del
SELECT from_id FROM links
WHERE to_id IS NOT NULL
AND from_id IS NOT NULL;

DELETE FROM account_agreements WHERE account_id IN (SELECT old_id FROM to_del);
DELETE FROM account_external_ids WHERE account_id IN (SELECT old_id FROM to_del);
DELETE FROM account_group_members WHERE account_id IN (SELECT old_id FROM to_del);
DELETE FROM account_project_watches WHERE account_id IN (SELECT old_id FROM to_del);
DELETE FROM account_ssh_keys WHERE account_id IN (SELECT old_id FROM to_del);
DELETE FROM accounts WHERE account_id IN (SELECT old_id FROM to_del);
DELETE FROM starred_changes WHERE account_id IN (SELECT old_id FROM to_del);
DELETE FROM patch_set_approvals WHERE account_id IN (SELECT old_id FROM to_del);
```
