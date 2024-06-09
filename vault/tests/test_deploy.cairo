use snforge_std::{ declare, ContractClassTrait, cheat_execution_info };
use vault::erc4626::interface::{IERC4626Dispatcher, IERC4626DispatcherTrait};
use openzeppelin::token::erc20::{ERC20ABIDispatcher, ERC20ABIDispatcherTrait};
use starknet::{ContractAddress, contract_address_const, get_contract_address};
use openzeppelin::utils::serde::SerializedAppend;
use vault::utils::{pow_256};
use core::integer::BoundedInt;


fn OWNER() -> ContractAddress {
    'owner'.try_into().unwrap()
}

fn TOKEN_ADDRESS() -> ContractAddress {
    'token_address'.try_into().unwrap()
}

fn INITIAL_SUPPLY() -> u256 {
    1000000000000000000000000000000
}

fn deploy_contract() -> (ERC20ABIDispatcher, IERC4626Dispatcher) {
    let (token, token_address) = deploy_token();
    //let asset_address = contract_address_const::<0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7>();
    let mut calldata = array![];
    let name: ByteArray = "ETH2X";
    let symbol: ByteArray = "ETH2X";
    calldata.append_serde(token_address);
    //calldata.append_serde(asset_address);
    calldata.append_serde(name);
    calldata.append_serde(symbol);
    calldata.append(0);

    let vault = declare("Vault").unwrap();
    let (contract_address, _) = vault.deploy(@calldata).unwrap();
    (token, IERC4626Dispatcher { contract_address })
}

fn deploy_token() -> (ERC20ABIDispatcher, ContractAddress) {
    let token = declare("ERC20Token").unwrap();
    let mut calldata = Default::default();
    Serde::serialize(@OWNER(), ref calldata);
    Serde::serialize(@INITIAL_SUPPLY(), ref calldata);

    let (address, _) = token.deploy_at(@calldata, TOKEN_ADDRESS()).unwrap();
    let dispatcher = ERC20ABIDispatcher { contract_address: address };
    (dispatcher, address)
}

#[test]
fn test_constructor() {
    let (asset, vault) = deploy_contract();
    assert(vault.asset() == asset.contract_address, 'invalid asset');
    assert(vault.decimals() == (18 + 0), 'invalid decimals');
    assert(vault.name() == "ETH2X", 'invalid name');
    assert(vault.symbol() == "ETH2X", 'invalid symbol');
}

#[test]
fn convert_to_assets() {
    let (_asset, vault) = deploy_contract();
    let shares = pow_256(10, 2);
    // 10e10 * (0 + 1) / (0 + 10e8)
    assert(vault.convert_to_assets(shares) == 100, 'invalid assets');
}
#[test]
fn convert_to_shares() {
    let (_asset, vault) = deploy_contract();
    let assets = 10;
    // asset * shares / total assets
    // 10 * (0 + 10e8) / (0 + 1)
    assert(vault.convert_to_shares(assets) == pow_256(10, 1), 'invalid shares');
}

#[test]
fn max_deposit() {
    let (_asset, vault) = deploy_contract();
    assert(vault.max_deposit(get_contract_address()) == BoundedInt::<u256>::max(), 'invalid max deposit');
}

#[test]
fn call_and_invoke() {
    // First declare and deploy a contract
    //let contract = declare("Vault").unwrap();

    let (_asset, dispatcher) = deploy_contract();

    // Create a Dispatcher object that will allow interacting with the deployed contract
    //let dispatcher = IERC4626Dispatcher { contract_address };
    //let dispatcher = IERC4626Dispatcher { contract_address };

    // Call a view function of the contract
    //let name = dispatcher.name();
    //assert(name == 0, 'name == 0');

    let decimals = dispatcher.decimals();
    println!("{}", decimals);
    assert(decimals == 18, 'decimals == 18');

    // Call a function of the contract
    // Here we mutate the state of the storage
    //dispatcher.increase_balance(100);

    // Check that transaction took effect
    //let balance = dispatcher.get_balance();
    //assert(balance == 100, 'balance == 100');
}