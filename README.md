# FTP-Client-Server-Application

This project is a Python-based implementation of a **File Transfer Protocol (FTP) client and server**, built to demonstrate networking fundamentals and client-server communication over **TCP connections**.  
The server supports **multiple concurrent clients** through multithreading and implements core FTP functionalities in compliance with **RFC 959**.

---

## 🚀 Features
- Multi-threaded **FTP server** capable of handling multiple client connections.
- **Core FTP functionalities**:
  - Upload files  
  - Download files  
  - Passive mode data transfer  
- Packet-level inspection with **Wireshark** for debugging and validation.
- Tested with standard FTP client **FileZilla**.
- Recommendations for secure alternatives (**SSL-FTP**, **SFTP**).

---

## 🛠️ Tech Stack
- **Programming Language:** Python 3.x  
- **Libraries/Modules:** `socket`, `threading`, `os`  
- **Tools:** Wireshark, FileZilla  
- **Protocol Standards:** TCP, FTP (RFC 959)


