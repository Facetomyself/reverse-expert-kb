# oracle-mail / CHANGELOG

- 2026-03-15: First-pass inspection completed. Confirmed `oracle-mail` (`140.83.52.216`) is an Oracle Linux 8.10 host with Docker running but no active containers or public mail/web listeners. Found a dormant Mailu deployment under `/root/mailu` and a separate `moemail` repository under `/root/moemail`. Public DNS currently points mail-related names here, but runtime does not match the expected exposed services.
