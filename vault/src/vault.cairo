#[starknet::interface]
pub trait IRebalanceTrait<TContractState> {
    fn rebalance(ref self:TContractState, leverage: bool);
}

#[starknet::contract]
mod Vault {
    use vault::erc4626::erc4626::{ERC4626Component};
    use openzeppelin::introspection::src5::SRC5Component;
    use openzeppelin::token::erc20::ERC20Component;
    use openzeppelin::token::erc20::interface::{IERC20, IERC20Dispatcher, IERC20DispatcherTrait};
    use starknet::{get_contract_address, ContractAddress, get_caller_address, contract_address_const};

    component!(path: ERC4626Component, storage: erc4626, event: ERC4626Event);
    component!(path: ERC20Component, storage: erc20, event: ERC20Event);
    component!(path: SRC5Component, storage: src5, event: SRC5Event);

    #[abi(embed_v0)]
    impl ERC4626AdditionalImpl = ERC4626Component::ERC4626AdditionalImpl<ContractState>;
    #[abi(embed_v0)]
    impl MetadataEntrypointsImpl = ERC4626Component::MetadataEntrypointsImpl<ContractState>;
    #[abi(embed_v0)]
    impl SnakeEntrypointsImpl = ERC4626Component::SnakeEntrypointsImpl<ContractState>;

    impl ERC4626InternalImpl = ERC4626Component::InternalImpl<ContractState>;

    #[abi(embed_v0)]
    impl RebalanceImpl of super::IRebalanceTrait<ContractState> {
        fn rebalance(ref self: ContractState, leverage: bool) {
            let caller = get_caller_address();
            assert(caller == contract_address_const::<0x00eA6b9d15886250e60a2eDF0Cb0673cb94306F350f78435f7112073e251C6Ed>(), 'unauthorized caller');
            // Integrate with Nostra or zkLend or zkx to leverage or deleverage
        }
    }


    #[storage]
    struct Storage {
        #[substorage(v0)]
        erc4626: ERC4626Component::Storage,
        #[substorage(v0)]
        erc20: ERC20Component::Storage,
        #[substorage(v0)]
        src5: SRC5Component::Storage,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        #[flat]
        ERC4626Event: ERC4626Component::Event,
        #[flat]
        ERC20Event: ERC20Component::Event,
        #[flat]
        SRC5Event: SRC5Component::Event,
    }

    #[constructor]
    fn constructor(
        ref self: ContractState,
        asset: ContractAddress,
        name: ByteArray,
        symbol: ByteArray,
        offset: u8,
    ) {
        self.erc4626.initializer(asset, name, symbol, offset);
    }
}