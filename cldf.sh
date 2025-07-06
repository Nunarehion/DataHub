user@Z:~$ warp-cli --help
CLI to the WARP service daemon

Usage: warp-cli [OPTIONS] <COMMAND>

Commands:
  connect               Maintain a connection whenever possible
  debug                 Debugging commands
  disconnect            Disconnect the client
  dns                   Configure DNS settings
  environment           Configure the WARP Client's compliance environment
  mdm                   MDM configs
  mode                  Set the client's general operating mode
  override              Allow temporary overrides of administrative settings
  proxy                 Configure proxy mode settings
  registration          Registration settings
  connector             Register a WARP Connector
  settings              Show or alter general application settings
  status                Return the current connection status
  target                Manage targets
  trusted               Configure trusted networks where the client will be automatically disabled (Consumer only)
  tunnel                Configure tunnel settings
  vnet                  Get or specify connected virtual network
  generate-completions  Generate completions for a given shell and print to stdout
  stats                 Display statistics for Cloudflare WARP
  certs                 Print all account certificates installed on the device to stdout
  help                  Print this message or the help of the given subcommand(s)

Options:
  -l, --listen
          Listen for status changes and DNS logs (if enabled)

      --accept-tos
          Accept the Terms of Service agreement

  -v, --verbose...
          Enable verbose output. Multiple "v"s adds more verbosity

  -j, --json
          Pretty print output as json

      --no-paginate
          Disable automatic pagination

      --no-ansi
          Disable ANSI characters in standard outputs

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version

Subcommands:

api:
  endpoint  Set an override endpoint for the WARP API
  help      Print this message or the help of the given subcommand(s)

connect:
  Maintain a connection whenever possible

debug:
  access-reauth       Force refresh authentication with Cloudflare Access
  alternate-network   Get the name of the currently detected alternate network, if any
  connectivity-check  Enable or disable connectivity checks
  dex                 Get the most recently uploaded DEX data. Returns the most recent test for each dex metric
  network             Display the current network information
  posture             Display the most recent device posture information
  pcap                Run a packet capture on the device
  qlog                Enable qlog logging on the tunnel, if supported by the tunnel protocol
  help                Print this message or the help of the given subcommand(s)

disconnect:
  Disconnect the client

dns:
  fallback           Configure fallback domains
  families           Configure Families Mode settings (Consumer only)
  gateway-id         Force the app to use the specified Gateway ID for DNS queries
  log                Enable/Disable DNS logging
  stats              Retrieve DNS stats for the current connection
  default-fallbacks  Display which DNS servers are being used for default fallback
  help               Print this message or the help of the given subcommand(s)

environment:
  set    Set the client's compliance environment
  reset  Reset the client's compliance environment override
  help   Print this message or the help of the given subcommand(s)

mdm:
  get-configs  Show information about current MDM configurations
  set-config   Apply config from configs found in MDM file
  help         Print this message or the help of the given subcommand(s)

mode:
  Set the client's general operating mode

override:
  show           Return information about any currently applied administrative override
  unlock         Temporarily override policies that require the client to stay enabled
  local-network  Override settings to access the local area network
  help           Print this message or the help of the given subcommand(s)

proxy:
  port  Override the listening port for proxy mode (127.0.0.1:{port})
  help  Print this message or the help of the given subcommand(s)

registration:
  show          Show information about the current registration
  new           Register this client (Must be run before first connection!)
  delete        Delete current registration
  organization  Get the name of the current Teams organization
  devices       Display the list of devices associated with the current registration
  license       Attach the current registration to a different account using a license key
  help          Print this message or the help of the given subcommand(s)

connector:
  new   Register a new WARP Connector
  help  Print this message or the help of the given subcommand(s)

settings:
  list                 Retrieve the current application settings
  reset                Restore settings to default
  support-url          Get the support url for the current Teams organization
  mode-switch-allowed  Outputs true if Teams users should be able to change connection mode, or false if not
  help                 Print this message or the help of the given subcommand(s)

status:
  Return the current connection status

target:
  list  List all available targets accessible by the current user
  help  Print this message or the help of the given subcommand(s)

trusted:
  ssid      Configure trusted Wi-Fi networks for which the client will be automatically disconnected
  ethernet  Automatically disconnect on all ethernet networks (disabled for Zero Trust customers)
  wifi      Automatically disconnect on all Wi-Fi networks (disabled for Zero Trust customers)
  help      Print this message or the help of the given subcommand(s)

tunnel:
  dump            Get split tunnel routing dump. For include-only mode, this shows routes NOT included
  host            Configure split tunnel hosts
  ip              Configure split tunnel IPs
  stats           Retrieve the stats for the current tunnel connection
  rotate-keys     Generate a new key-pair, keeping the current registration
  endpoint        Force the client to connect to the specified IP:PORT endpoint (Zero Trust customers must run this command as a privileged user)
  protocol        Modify the preferred tunnel protocol (Consumer only)
  masque-options  Modify the MASQUE tunnel protocol options (Consumer only)
  help            Print this message or the help of the given subcommand(s)

vnet:
  Get or specify connected virtual network

generate-completions:
  Generate completions for a given shell and print to stdout

stats:
  Display statistics for Cloudflare WARP

certs:
  Print all account certificates installed on the device to stdout
user@Z:~$ 
