# Requirements: Send the CardDemo test file by FTP (SOM-C04)

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
