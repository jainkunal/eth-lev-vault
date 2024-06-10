from starknet_py.abi.v2 import AbiParser

abi = [
    {
        "name": "RebalanceImpl",
        "type": "impl",
        "interface_name": "vault::vault::IRebalanceTrait",
    },
    {
        "name": "core::bool",
        "type": "enum",
        "variants": [{"name": "False", "type": "()"}, {"name": "True", "type": "()"}],
    },
    {
        "name": "vault::vault::IRebalanceTrait",
        "type": "interface",
        "items": [
            {
                "name": "rebalance",
                "type": "function",
                "inputs": [{"name": "leverage", "type": "core::bool"}],
                "outputs": [],
                "state_mutability": "external",
            }
        ],
    },
    {
        "name": "ERC4626AdditionalImpl",
        "type": "impl",
        "interface_name": "vault::erc4626::interface::IERC4626Additional",
    },
    {
        "name": "core::integer::u256",
        "type": "struct",
        "members": [
            {"name": "low", "type": "core::integer::u128"},
            {"name": "high", "type": "core::integer::u128"},
        ],
    },
    {
        "name": "vault::erc4626::interface::IERC4626Additional",
        "type": "interface",
        "items": [
            {
                "name": "asset",
                "type": "function",
                "inputs": [],
                "outputs": [
                    {"type": "core::starknet::contract_address::ContractAddress"}
                ],
                "state_mutability": "view",
            },
            {
                "name": "convert_to_assets",
                "type": "function",
                "inputs": [{"name": "shares", "type": "core::integer::u256"}],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "convert_to_shares",
                "type": "function",
                "inputs": [{"name": "assets", "type": "core::integer::u256"}],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "deposit",
                "type": "function",
                "inputs": [
                    {"name": "assets", "type": "core::integer::u256"},
                    {
                        "name": "receiver",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "external",
            },
            {
                "name": "max_deposit",
                "type": "function",
                "inputs": [
                    {
                        "name": "address",
                        "type": "core::starknet::contract_address::ContractAddress",
                    }
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "max_mint",
                "type": "function",
                "inputs": [
                    {
                        "name": "receiver",
                        "type": "core::starknet::contract_address::ContractAddress",
                    }
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "max_redeem",
                "type": "function",
                "inputs": [
                    {
                        "name": "owner",
                        "type": "core::starknet::contract_address::ContractAddress",
                    }
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "max_withdraw",
                "type": "function",
                "inputs": [
                    {
                        "name": "owner",
                        "type": "core::starknet::contract_address::ContractAddress",
                    }
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "mint",
                "type": "function",
                "inputs": [
                    {"name": "shares", "type": "core::integer::u256"},
                    {
                        "name": "receiver",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "external",
            },
            {
                "name": "preview_deposit",
                "type": "function",
                "inputs": [{"name": "assets", "type": "core::integer::u256"}],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "preview_mint",
                "type": "function",
                "inputs": [{"name": "shares", "type": "core::integer::u256"}],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "preview_redeem",
                "type": "function",
                "inputs": [{"name": "shares", "type": "core::integer::u256"}],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "preview_withdraw",
                "type": "function",
                "inputs": [{"name": "assets", "type": "core::integer::u256"}],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "redeem",
                "type": "function",
                "inputs": [
                    {"name": "shares", "type": "core::integer::u256"},
                    {
                        "name": "receiver",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                    {
                        "name": "owner",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "external",
            },
            {
                "name": "total_assets",
                "type": "function",
                "inputs": [],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "withdraw",
                "type": "function",
                "inputs": [
                    {"name": "assets", "type": "core::integer::u256"},
                    {
                        "name": "receiver",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                    {
                        "name": "owner",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "external",
            },
        ],
    },
    {
        "name": "MetadataEntrypointsImpl",
        "type": "impl",
        "interface_name": "vault::erc4626::interface::IERC4626Metadata",
    },
    {
        "name": "core::byte_array::ByteArray",
        "type": "struct",
        "members": [
            {"name": "data", "type": "core::array::Array::<core::bytes_31::bytes31>"},
            {"name": "pending_word", "type": "core::felt252"},
            {"name": "pending_word_len", "type": "core::integer::u32"},
        ],
    },
    {
        "name": "vault::erc4626::interface::IERC4626Metadata",
        "type": "interface",
        "items": [
            {
                "name": "name",
                "type": "function",
                "inputs": [],
                "outputs": [{"type": "core::byte_array::ByteArray"}],
                "state_mutability": "view",
            },
            {
                "name": "symbol",
                "type": "function",
                "inputs": [],
                "outputs": [{"type": "core::byte_array::ByteArray"}],
                "state_mutability": "view",
            },
            {
                "name": "decimals",
                "type": "function",
                "inputs": [],
                "outputs": [{"type": "core::integer::u8"}],
                "state_mutability": "view",
            },
        ],
    },
    {
        "name": "SnakeEntrypointsImpl",
        "type": "impl",
        "interface_name": "vault::erc4626::interface::IERC4626Snake",
    },
    {
        "name": "vault::erc4626::interface::IERC4626Snake",
        "type": "interface",
        "items": [
            {
                "name": "total_supply",
                "type": "function",
                "inputs": [],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "balance_of",
                "type": "function",
                "inputs": [
                    {
                        "name": "account",
                        "type": "core::starknet::contract_address::ContractAddress",
                    }
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "allowance",
                "type": "function",
                "inputs": [
                    {
                        "name": "owner",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                    {
                        "name": "spender",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                ],
                "outputs": [{"type": "core::integer::u256"}],
                "state_mutability": "view",
            },
            {
                "name": "transfer",
                "type": "function",
                "inputs": [
                    {
                        "name": "recipient",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                    {"name": "amount", "type": "core::integer::u256"},
                ],
                "outputs": [{"type": "core::bool"}],
                "state_mutability": "external",
            },
            {
                "name": "transfer_from",
                "type": "function",
                "inputs": [
                    {
                        "name": "sender",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                    {
                        "name": "recipient",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                    {"name": "amount", "type": "core::integer::u256"},
                ],
                "outputs": [{"type": "core::bool"}],
                "state_mutability": "external",
            },
            {
                "name": "approve",
                "type": "function",
                "inputs": [
                    {
                        "name": "spender",
                        "type": "core::starknet::contract_address::ContractAddress",
                    },
                    {"name": "amount", "type": "core::integer::u256"},
                ],
                "outputs": [{"type": "core::bool"}],
                "state_mutability": "external",
            },
        ],
    },
    {
        "name": "constructor",
        "type": "constructor",
        "inputs": [
            {
                "name": "asset",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {"name": "name", "type": "core::byte_array::ByteArray"},
            {"name": "symbol", "type": "core::byte_array::ByteArray"},
            {"name": "offset", "type": "core::integer::u8"},
        ],
    },
    {
        "kind": "struct",
        "name": "vault::erc4626::erc4626::ERC4626Component::Deposit",
        "type": "event",
        "members": [
            {
                "kind": "key",
                "name": "sender",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {
                "kind": "key",
                "name": "owner",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {"kind": "data", "name": "assets", "type": "core::integer::u256"},
            {"kind": "data", "name": "shares", "type": "core::integer::u256"},
        ],
    },
    {
        "kind": "struct",
        "name": "vault::erc4626::erc4626::ERC4626Component::Withdraw",
        "type": "event",
        "members": [
            {
                "kind": "key",
                "name": "sender",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {
                "kind": "key",
                "name": "receiver",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {
                "kind": "key",
                "name": "owner",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {"kind": "data", "name": "assets", "type": "core::integer::u256"},
            {"kind": "data", "name": "shares", "type": "core::integer::u256"},
        ],
    },
    {
        "kind": "enum",
        "name": "vault::erc4626::erc4626::ERC4626Component::Event",
        "type": "event",
        "variants": [
            {
                "kind": "nested",
                "name": "Deposit",
                "type": "vault::erc4626::erc4626::ERC4626Component::Deposit",
            },
            {
                "kind": "nested",
                "name": "Withdraw",
                "type": "vault::erc4626::erc4626::ERC4626Component::Withdraw",
            },
        ],
    },
    {
        "kind": "struct",
        "name": "openzeppelin::token::erc20::erc20::ERC20Component::Transfer",
        "type": "event",
        "members": [
            {
                "kind": "key",
                "name": "from",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {
                "kind": "key",
                "name": "to",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {"kind": "data", "name": "value", "type": "core::integer::u256"},
        ],
    },
    {
        "kind": "struct",
        "name": "openzeppelin::token::erc20::erc20::ERC20Component::Approval",
        "type": "event",
        "members": [
            {
                "kind": "key",
                "name": "owner",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {
                "kind": "key",
                "name": "spender",
                "type": "core::starknet::contract_address::ContractAddress",
            },
            {"kind": "data", "name": "value", "type": "core::integer::u256"},
        ],
    },
    {
        "kind": "enum",
        "name": "openzeppelin::token::erc20::erc20::ERC20Component::Event",
        "type": "event",
        "variants": [
            {
                "kind": "nested",
                "name": "Transfer",
                "type": "openzeppelin::token::erc20::erc20::ERC20Component::Transfer",
            },
            {
                "kind": "nested",
                "name": "Approval",
                "type": "openzeppelin::token::erc20::erc20::ERC20Component::Approval",
            },
        ],
    },
    {
        "kind": "enum",
        "name": "openzeppelin::introspection::src5::SRC5Component::Event",
        "type": "event",
        "variants": [],
    },
    {
        "kind": "enum",
        "name": "vault::vault::Vault::Event",
        "type": "event",
        "variants": [
            {
                "kind": "flat",
                "name": "ERC4626Event",
                "type": "vault::erc4626::erc4626::ERC4626Component::Event",
            },
            {
                "kind": "flat",
                "name": "ERC20Event",
                "type": "openzeppelin::token::erc20::erc20::ERC20Component::Event",
            },
            {
                "kind": "flat",
                "name": "SRC5Event",
                "type": "openzeppelin::introspection::src5::SRC5Component::Event",
            },
        ],
    },
]
abi = AbiParser(abi).parse()
