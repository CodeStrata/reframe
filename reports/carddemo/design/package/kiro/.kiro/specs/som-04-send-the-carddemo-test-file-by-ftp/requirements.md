# Requirements: Send the CardDemo test file by FTP (SOM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as scheduled job · risk high

## Introduction

Operations sends the CardDemo test file to a remote FTP folder to prove the outbound file-transfer path works: it signs on as 'carddemousr' and delivers the file as text named 'welcome.txt' into '/ftpfolder'. It must deliver the file under the right name and in text mode, and must never leave the transfer session open. The sign-on details should come from managed secrets, not be written into the job.

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
