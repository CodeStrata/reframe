# Send the CardDemo test file by FTP (SOM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as scheduled job · risk high

## Introduction

Is an operations job that sends the CardDemo test file to a remote FTP folder, to prove that outbound file transfer works. It is for operations administrators, not end users. It must deliver the file as text to '/ftpfolder' under the name 'welcome.txt' on the configured server, and must keep the sign-on credentials out of the job definition.

**User story:** As an operations administrator, I want the CardDemo test dataset sent to the remote FTP folder, so that the file transfer path can be exercised.

## Requirements

### Requirement 1: SOM-REQ-F-026 (business rule)

#### Acceptance criteria

1. The system shall sign on to the FTP server 172.31.21.124 as user 'carddemousr', switch to text (ASCII) mode, list the current remote folder and its contents, and change to the remote folder '/ftpfolder'. (rules SOM-BR-030)
2. GIVEN Server: 172.31.21.124; User: carddemousr WHEN Outbound File Transfer runs THEN The session is signed on in ASCII mode and positioned in /ftpfolder (SOM-C04-AC-01; SOM-BR-030)

### Requirement 2: SOM-REQ-F-027 (side effect)

#### Acceptance criteria

1. While the transfer session is positioned in '/ftpfolder', the system shall send the mainframe dataset 'AWS.M2.CARDEMO.FTP.TEST' to that folder as 'welcome.txt' and then end the session (QUIT). (rules SOM-BR-031)
2. GIVEN Dataset: AWS.M2.CARDEMO.FTP.TEST WHEN the transfer session is positioned in '/ftpfolder' THEN The remote folder /ftpfolder holds welcome.txt with the dataset content as text (SOM-C04-AC-02; SOM-BR-031)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-030 | Send card demo test file to remote folder | business rule | THE Outbound File Transfer SHALL sign on to the FTP server 172.31.21.124 as user 'carddemousr', switch to text (ASCII) mode, list the current remote folder and its contents, and change to the remote folder '/ftpfolder'. | medium | app/jcl/FTPJCL.JCL:30-41, app/jcl/FTPJCL.JCL:21-29 |
| SOM-BR-031 | Send card demo test file to remote folder | side effect | WHEN the transfer session is positioned in '/ftpfolder', THE Outbound File Transfer SHALL send the mainframe dataset 'AWS.M2.CARDEMO.FTP.TEST' to that folder as 'welcome.txt' and then end the session (QUIT). | medium | app/jcl/FTPJCL.JCL:30-41, app/jcl/FTPJCL.JCL:21-29 |

### Worked examples

- SOM-BR-030: Server = 172.31.21.124; User = carddemousr → The session is signed on in ASCII mode and positioned in /ftpfolder
- SOM-BR-031: Dataset = AWS.M2.CARDEMO.FTP.TEST → The remote folder /ftpfolder holds welcome.txt with the dataset content as text

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-261: If the file transfer of welcome.txt fails at sign-on, mode setting, folder change or send, what should happen: report failure, retry, or leave a partial file on the remote server? (System operations) On SOM-BR-031.
- SME-262: If welcome.txt already exists in the remote folder, should the transfer overwrite it, keep a version, or refuse? (System operations) On SOM-BR-031.
- SME-263: Which remote server, target folder and sign-on identity should the new file transfer use? (System operations) On SOM-BR-031.
- DEF-149: Confirm this is deliberate: The FTP user's password is written in clear text in the job input and sent over unencrypted FTP; also the header comment calls this a job to receive a file although it sends one. (Subject-matter expert) On SOM-BR-031.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).
