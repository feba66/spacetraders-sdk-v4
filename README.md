


```sh
make
```



| Class          | Method                                                                              | Description                   | sdk      | redis                  | postgres |
| -------------- | ----------------------------------------------------------------------------------- | ----------------------------- | -------- | ---------------------- | -------- |
| *AgentsApi*    | [**get_agent**](docs/AgentsApi.md#get_agent)                                        | Get Public Agent              |
| *AgentsApi*    | [**get_agents**](docs/AgentsApi.md#get_agents)                                      | List Agents                   |
| *AgentsApi*    | [**get_my_agent**](docs/AgentsApi.md#get_my_agent)                                  | Get Agent                     | x        | x                      |
| *ContractsApi* | [**accept_contract**](docs/ContractsApi.md#accept_contract)                         | Accept Contract               | x        |
| *ContractsApi* | [**deliver_contract**](docs/ContractsApi.md#deliver_contract)                       | Deliver Cargo to Contract     | x        |
| *ContractsApi* | [**fulfill_contract**](docs/ContractsApi.md#fulfill_contract)                       | Fulfill Contract              | x        |
| *ContractsApi* | [**get_contract**](docs/ContractsApi.md#get_contract)                               | Get Contract                  |
| *ContractsApi* | [**get_contracts**](docs/ContractsApi.md#get_contracts)                             | List Contracts                | x        |
| *FactionsApi*  | [**get_faction**](docs/FactionsApi.md#get_faction)                                  | Get Faction                   |
| *FactionsApi*  | [**get_factions**](docs/FactionsApi.md#get_factions)                                | List Factions                 |
| *FleetApi*     | [**create_chart**](docs/FleetApi.md#create_chart)                                   | Create Chart                  |
| *FleetApi*     | [**create_ship_ship_scan**](docs/FleetApi.md#create_ship_ship_scan)                 | Scan Ships                    |
| *FleetApi*     | [**create_ship_system_scan**](docs/FleetApi.md#create_ship_system_scan)             | Scan Systems                  |
| *FleetApi*     | [**create_ship_waypoint_scan**](docs/FleetApi.md#create_ship_waypoint_scan)         | Scan Waypoints                |
| *FleetApi*     | [**create_survey**](docs/FleetApi.md#create_survey)                                 | Create Survey                 |
| *FleetApi*     | [**dock_ship**](docs/FleetApi.md#dock_ship)                                         | Dock Ship                     | x        | x                      |
| *FleetApi*     | [**extract_resources**](docs/FleetApi.md#extract_resources)                         | Extract Resources             |
| *FleetApi*     | [**extract_resources_with_survey**](docs/FleetApi.md#extract_resources_with_survey) | Extract Resources with Survey |
| *FleetApi*     | [**get_mounts**](docs/FleetApi.md#get_mounts)                                       | Get Mounts                    |
| *FleetApi*     | [**get_my_ship**](docs/FleetApi.md#get_my_ship)                                     | Get Ship                      |
| *FleetApi*     | [**get_my_ship_cargo**](docs/FleetApi.md#get_my_ship_cargo)                         | Get Ship Cargo                |
| *FleetApi*     | [**get_my_ships**](docs/FleetApi.md#get_my_ships)                                   | List Ships                    | x        | x                      |
| *FleetApi*     | [**get_repair_ship**](docs/FleetApi.md#get_repair_ship)                             | Get Repair Ship               |
| *FleetApi*     | [**get_scrap_ship**](docs/FleetApi.md#get_scrap_ship)                               | Get Scrap Ship                |
| *FleetApi*     | [**get_ship_cooldown**](docs/FleetApi.md#get_ship_cooldown)                         | Get Ship Cooldown             |
| *FleetApi*     | [**get_ship_nav**](docs/FleetApi.md#get_ship_nav)                                   | Get Ship Nav                  |
| *FleetApi*     | [**install_mount**](docs/FleetApi.md#install_mount)                                 | Install Mount                 |
| *FleetApi*     | [**jettison**](docs/FleetApi.md#jettison)                                           | Jettison Cargo                |
| *FleetApi*     | [**jump_ship**](docs/FleetApi.md#jump_ship)                                         | Jump Ship                     |
| *FleetApi*     | [**navigate_ship**](docs/FleetApi.md#navigate_ship)                                 | Navigate Ship                 | x        | x                      |
| *FleetApi*     | [**negotiate_contract**](docs/FleetApi.md#negotiate_contract)                       | Negotiate Contract            | x        |
| *FleetApi*     | [**orbit_ship**](docs/FleetApi.md#orbit_ship)                                       | Orbit Ship                    | x        | x                      |
| *FleetApi*     | [**patch_ship_nav**](docs/FleetApi.md#patch_ship_nav)                               | Patch Ship Nav                |
| *FleetApi*     | [**purchase_cargo**](docs/FleetApi.md#purchase_cargo)                               | Purchase Cargo                | x        | x                      |
| *FleetApi*     | [**purchase_ship**](docs/FleetApi.md#purchase_ship)                                 | Purchase Ship                 | x        | x                      |
| *FleetApi*     | [**refuel_ship**](docs/FleetApi.md#refuel_ship)                                     | Refuel Ship                   | x        | x, cargo not returned? |
| *FleetApi*     | [**remove_mount**](docs/FleetApi.md#remove_mount)                                   | Remove Mount                  |
| *FleetApi*     | [**repair_ship**](docs/FleetApi.md#repair_ship)                                     | Repair Ship                   |
| *FleetApi*     | [**scrap_ship**](docs/FleetApi.md#scrap_ship)                                       | Scrap Ship                    |
| *FleetApi*     | [**sell_cargo**](docs/FleetApi.md#sell_cargo)                                       | Sell Cargo                    | x        | x                      |
| *FleetApi*     | [**ship_refine**](docs/FleetApi.md#ship_refine)                                     | Ship Refine                   |
| *FleetApi*     | [**siphon_resources**](docs/FleetApi.md#siphon_resources)                           | Siphon Resources              |
| *FleetApi*     | [**transfer_cargo**](docs/FleetApi.md#transfer_cargo)                               | Transfer Cargo                |
| *FleetApi*     | [**warp_ship**](docs/FleetApi.md#warp_ship)                                         | Warp Ship                     |
| *SystemsApi*   | [**get_construction**](docs/SystemsApi.md#get_construction)                         | Get Construction Site         |
| *SystemsApi*   | [**get_jump_gate**](docs/SystemsApi.md#get_jump_gate)                               | Get Jump Gate                 |
| *SystemsApi*   | [**get_market**](docs/SystemsApi.md#get_market)                                     | Get Market                    | x        | x                      |
| *SystemsApi*   | [**get_shipyard**](docs/SystemsApi.md#get_shipyard)                                 | Get Shipyard                  | x        | x                      |
| *SystemsApi*   | [**get_system**](docs/SystemsApi.md#get_system)                                     | Get System                    | x        | x                      |
| *SystemsApi*   | [**get_system_waypoints**](docs/SystemsApi.md#get_system_waypoints)                 | List Waypoints in System      | x        | x                      |
| *SystemsApi*   | [**get_systems**](docs/SystemsApi.md#get_systems)                                   | List Systems                  |
| *SystemsApi*   | [**get_waypoint**](docs/SystemsApi.md#get_waypoint)                                 | Get Waypoint                  |
| *SystemsApi*   | [**supply_construction**](docs/SystemsApi.md#supply_construction)                   | Supply Construction Site      |
| *DefaultApi*   | [**get_status**](docs/DefaultApi.md#get_status)                                     | Get Status                    |          |
| *DefaultApi*   | [**register**](docs/DefaultApi.md#register)                                         | Register New Agent            | outdated |



### Mindstorming

- influxdb for stats that are nice to show in a diagramm
  - credits every time they change
  - buy/sell goods
  - ship count (per ship type)
  - 
- history in postgres
  - surveys
  - extracts
  - fuel usage
  - nav time
- state in redis

- some form of backend which takes care of state, history, stats, logging etc
- a dashboard of some sort which shows trades, some stats etc

- trading logic for multiple ships

- some form of ship task list, to store that and resume on restart of client

- pathfinding service, with cache for explored routes

- "workers"
  - ship buy and mount swapping
  - trading
    - for profit
    - to fire up the markets
  - surveying
  - mining
  - transporters for mining
  - contracts
  - fuel hauling?
  - probe deploying
  - market & shipyard polling
  - gate building

- Logic to handle a reset, preferably automatically...

- backend frontend communication either via rest or sockets

#### Components
- Gateway (Backend. Running on the server, ratelimit, state etc. So that you can start a "Dashboard" locally)
- Dashboard (Frontend which gets its data from the gateway)
- Pathfinding Service (A*, cost via Fuel, Time or Requests. Caching)
- Trade Route Service (Maybe Traveling Salesman?, sortable by profit, profit/time and/or profit/request)
- Some form of control panel, maybe integrate into dashboard. (to decide what ships should do etc. Or manual commands)
