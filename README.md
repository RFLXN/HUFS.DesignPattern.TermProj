# HUFS Design Pattern Term Project
by 컴퓨터 전자시스템공학부 202004520 최준혁

# Structure
* document/ : All Documents Here.
* resource/ : DB Files, API Info, or ETC. Resource Files.
* repl/ : repl Python Package.
  * cmd_exec.py : CommandExecutor Class File
  * parser.py : CommandParser Class File
  * exception.py : Exception Classes File
* db/ : db Python Package.
  * scan_id.py : ScanIdDB Class File
* command/ : command Python Package.
  * abs.py : Command Abstract Class File
  * factory.py : CommandFactory Class File
  * result.py : CommandResult Class File
  * exception.py : Exception Classes File
  * type/ : type Python Package. Package for API Response JSON Wrapper Classes
  * real/ : real Python Package. Package for Concrete Commands
* api/ : api Python Package. Package for API Wrapper.
  * api_store.py : ApiInfoStore, ApiKeyStore Class File
  * api_type.py : ApiEndpoint Class File
  * request_sender.py : ApiRequestSender Class File
  * client.py : ApiClient Class File
* util/ : util Python Package. Package for Utility Functions
* structure/ : structure Python Package. Package for Design Pattern Structure. (ex: Singleton Meta Class)
* Pipfile : pipenv Dependency File.
* main.py : Entry File. Run this Code for Use Application.