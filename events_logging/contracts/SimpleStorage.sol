// SPDX-Liscence_Identifier:MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 public favoriteNumber;

    // can have max of 3 indexed vars
    event storedNumber(
        uint256 indexed oldNumber,
        uint256 indexed newNumber,
        uint256 addedNumber,
        address sender
    );

    function store(uint256 _favoritenNumber) public {
        emit storedNumber(
            favoriteNumber,
            _favoritenNumber,
            favoriteNumber + favoriteNumber,
            msg.sender
        );
        favoriteNumber = _favoritenNumber;
    }
}
