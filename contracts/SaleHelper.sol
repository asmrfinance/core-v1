// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IAltruisticSale {
    function updateCharity(address charity, bool status) external;
    function updateAdmin(address _to) external;
}

/// @title Sale helper
/// @author asmr.finance
/// @notice Used to set list of charities in efficient way
contract SaleHelper {
    address public admin;

    modifier onlyOwner() {
        require(msg.sender == admin, "SaleHelper: Not admin");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    /// @notice Append charities list
    /// @dev Transfers contract ownership after charities appended
    /// @param sale Sale contract
    /// @param charities Array of charities
    function updateCharity(IAltruisticSale sale, address[] calldata charities) external onlyOwner {
        for (uint256 i; i < charities.length; i++) {
            sale.updateCharity(charities[i], true);
        }
        updateAdmin(sale, msg.sender);
    }

    /// @notice Update admin of sale contract
    /// @param sale Sale contract
    /// @param _to New admin
    function updateAdmin(IAltruisticSale sale, address _to) public onlyOwner {
        sale.updateAdmin(_to);
    }
}