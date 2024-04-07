---
layout: post
title: "Tic-Tac-Toe with Reusable Components and Customizable Logic"
categories: [Infrastructure]
image: assets/images/tic-tac-toe.png
tags: [featured]
---

In this article, we showcase a simple game example developed using the Bolt Entity Component System (ECS), which facilitates reusability of components and enables users to modify and enhance the game's logic.

Furthermore, the framework significantly simplifies Solana development by abstracting low-level concepts such as account space and [Program Derived Addresses (PDAs)](https://solanacookbook.com/core-concepts/pdas.html#facts). For a comparison with an Anchor-based program, refer to this [tutorial](https://book.anchor-lang.com/anchor_in_depth/milestone_project_tic-tac-toe.html).

For a more detailed explanation of Bolt, see the announcement [blog post](/bolt-v0.1).

# Implementing Tic-Tac-Toe

The first section of this post details the implementation of the game logic using the Bolt framework. The second section explains how to integrate a React-based client with the program, starting with an open-source [Tic-Tac-Toe](https://github.com/ucfx/TIC-TAC-TOE-GAME) implementation.

The complete source code of the example is available [here](https://github.com/magicblock-labs/bolt-tic-tac-toe).

## The Game Logic: Implementing Tic-Tac-Toe with the Bolt ECS

First, install the `bolt-cli` with:

```bash
npm install @magicblock-labs/bolt-cli
```

Once installed, create a new project with:

```bash
bolt init tic-tac-toe
```

### Creating the Components

We need to define the data structures required. For simplicity, we will create two components: one containing the active players and the other containing the grid information.

Create a new components with:

```bash
bolt component players
```

This command creates a players component under program-ecs/components. The players component, which holds the public keys of the two players, can be defined as follows:


```rust
use bolt_lang::*;

declare_id!("5Xz6iiE2FZdpqrvCKbGqDajNYt1tP8cRGXrq3THSFo1q");

#[component]
#[derive(Default)]
pub struct Players {
    pub players: [Option<Pubkey>; 2],
}
```

The second component contains the grid information. Create it with:

```bash
bolt component grid
```

The grid component can be defined as:

```rust
use bolt_lang::*;

declare_id!("rdiVoU6KomhXBDMLi6UXVHvmjEUtKqb5iDCWChxMzZ7");

#[component]
pub struct Grid {
    pub board: [[Option<Sign>; 3]; 3],
    pub state: GameState,
    pub is_first_player_turn: bool,
}

#[component_deserialize]
#[derive(PartialEq)]
pub enum GameState {
    Active,
    Tie,
    Won { winner: Pubkey },
}

#[component_deserialize]
#[derive(PartialEq)]
pub enum Sign {
    X,
    O,
}

impl Sign {
    pub fn from_usize(value: usize) -> Sign {
        match value {
            0 => Sign::X,
            _ => Sign::O,
        }
    }
}

impl Default for Grid {
    fn default() -> Self {
        Self::new(GridInit{
            board: [[None; 3]; 3],
            state: GameState::Active,
            is_first_player_turn: true,
        })
    }
}
```

### Creating the Systems

Systems implement the game logic in a modular fashion. They operate on a bundle of input components and can perform any computation. Systems are executed in your world instance subject to the approval policy, e.g., a world could allow anyone to submit new systems, while another could require approval from a DAO.

The first system we build will allow a player to join a match:


```bash
bolt system join-game
```

Modify the logic (in program-ecs/systems/join-game.rs) to:

```rust
#[system]
pub mod join_game {

    pub fn execute(ctx: Context<Components>, _args_p: Vec<u8>) -> Result<Components> {
        let players = &mut ctx.accounts.players.players;
        let idx = match players.iter_mut().position(|player| player.is_none()) {
            Some(player_index) => player_index,
            None => return Err(PlayersError::GameFull.into()),
        };
        ctx.accounts.players.players[idx] = Some(*ctx.accounts.authority.key);
        Ok(ctx.accounts)
    }

    #[system_input]
    pub struct Components {
        pub players: Players,
    }

}
```

The second system implements the core logic of the game:

1. Create a play system:    
   
    ```bash 
    bolt system play
    ```
2. implement the logic:

```rust
use bolt_lang::*;
use grid::Grid;
use players::Players;

declare_id!("DyUy1naq1kb3r7HYBrTf7YhnGMJ5k5NqS3Mhk65GfSih");

#[system]
pub mod play {

    pub fn execute(ctx: Context<Components>, args: Args) -> Result<Components> {
        let grid = &mut ctx.accounts.grid;
        let players = &mut ctx.accounts.players;
        let authority = *ctx.accounts.authority.key;
        require!(players.players[0] == Some(authority) || players.players[1] == Some(authority), TicTacToeError::NotInGame);
        require!(grid.state == grid::GameState::Active, TicTacToeError::NotActive);
        let player_idx : usize = if players.players[0] == Some(authority) { 0 } else { 1 };
        require!(grid.is_first_player_turn == (player_idx == 0), TicTacToeError::NotPlayersTurn);

        // Core game logic
        match args {
            tile @ Args {
                row: 0..=2,
                column: 0..=2,
            } => match grid.board[tile.row as usize][tile.column as usize] {
                Some(_) => return Err(TicTacToeError::TileAlreadySet.into()),
                None => {
                    grid.board[tile.row as usize][tile.column as usize] =
                        Some(grid::Sign::from_usize(player_idx));
                }
            },
            _ => return Err(TicTacToeError::TileOutOfBounds.into()),
        }
        grid.is_first_player_turn = !grid.is_first_player_turn;
        check_winner(grid, authority);
        Ok(ctx.accounts)
    }

    #[system_input]
    pub struct Components {
        pub grid: Grid,
        pub players: Players,
    }

    #[arguments]
    struct Args {
        row: u8,
        column: u8,
    }

}

pub fn check_winner(grid: &mut Account<Grid>, player: Pubkey) {
    ...
}
```

Refer to the full [source code](https://github.com/magicblock-labs/bolt-tic-tac-toe/blob/main/programs-ecs/systems/play/src/lib.rs) for details.

As you can notice, the implementation is incredibly simple. The struct marked with `system_input` define the components input bundle, that can be accessed and used in the `execute` function. the struct marked with `arguments` define the arguments that your system can receive as input.

### Build and Test the Program

Build the program with:

```bash
bolt build
```

This command compiles the program and generates the IDL and TypeScript types automatically for client integration.

The process for setting up components and executing the systems involves the following steps:

1. Instantiate a world.
2. Create a match entity.
3. Attach the players and grid components to this match entity.
4. Execute the systems to facilitate gameplay.

The TypeScript tests for the Tic-Tac-Toe game can be found here:

### Connect a React Client

Connecting a React client is straightforward, thanks to the dynamic retrieval and generation of types and the utility functions provided by the Bolt TypeScript SDK.

Add the dependency with:

```bash
yarn add -D @magicblock-labs/bolt-sdk
```

For example, to execute a system:

```typescript
// Components
const GRID_COMPONENT = new PublicKey("rdiVoU6KomhXBDMLi6UXVHvmjEUtKqb5iDCWChxMzZ7");
const PLAYERS_COMPONENT = new PublicKey("5Xz6iiE2FZdpqrvCKbGqDajNYt1tP8cRGXrq3THSFo1q");

// Systems
const JOIN_GAME = new PublicKey("2umhnxiCtmg5KTn4L9BLo24uLjb74gAh4tmpMLRKYndN");
const PLAY = new PublicKey("DyUy1naq1kb3r7HYBrTf7YhnGMJ5k5NqS3Mhk65GfSih");

const applySystem = await ApplySystem({
    authority: publicKey,
    system: JOIN_GAME,
    entity,
    components: [PLAYERS_COMPONENT],
});
const transaction = applySystem.transaction;
const signature = await submitTransaction(transaction);
```

Find the simple Tic-Tac-Toe UI made in React here: [react-tic-tac-toe](https://github.com/magicblock-labs/bolt-tic-tac-toe/tree/main/app/react-tic-tac-toe)

An important aspect to highlight is that executing systems and instantiating components require only the ID. This means that new logic and data structures can be created and utilized dynamically, enabling the development of mods and alterations to your game's behavior.

### Conclusion

We have walked through a simple implementation of a Tic-Tac-Toe game using the Bolt ECS, demonstrating how to connect it to a React UI. This highlights the simplicity and flexibility of the framework, especially its potential for mods and user-generated logic, such as building a modified version of the game where players can make two moves each turn.
