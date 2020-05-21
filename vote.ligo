const owner : address = ("tz1fdtrrRmVFA1xGLgKi33UqT9LjQRZneXrc" : address);

type storage is record [
  status : bool;
  oui : nat;
  non : nat;
  voters : set(address);
]

type parameter is
| Vote of nat
| Reset of unit
| Stdby of string


type return is list (operation) * storage

function setVoters(const store : storage) : storage is 
block { 
  store.voters := Set.add (sender, store.voters)
} with store

function count(const store : storage; const vote : nat) : storage is
block {
  if vote = 1n
    then store.oui := store.oui + 1n
  else if vote = 2n then
    store.non := store.non + 1n
  else skip;
} with store

function break (const stat : string; const store : storage) : storage is
 block { 
   if sender =/= owner
   then failwith("No permissions.")
   else if sender = owner and stat = "True"
      then 
        if stat = "True" then
          store.status := True
        else if stat = "False" then 
          store.status := False
        else skip;
    else skip;
    } with store

function vote (const vote : nat; const store : storage) : storage is
block {
    if sender = owner or store.voters contains sender or store.status = False
      then failwith ("No permissions.")
    else skip;
    const cardinal : nat = Set.size(store.voters);
    if cardinal >= 10n 
      then 
        if store.oui > store.non 
          then failwith("Yes won")
        else failwith("No won")
    else if cardinal = 9n 
      then {
        store := setVoters(store);
        if vote = 1n
          then store.oui := store.oui + 1n
        else if vote = 2n then
          store.non := store.non + 1n
        else skip;

        if store.oui > store.non then 
          failwith("Yes") //yes win
        else 
          failwith("No"); //yes win
        
        // we reach 10 vote we can now block the vote
        store.status := False;
      } 
    else {
      store := setVoters(store);
      if vote = 1n
        then store.oui := store.oui + 1n
      else if vote = 2n then
        store.non := store.non + 1n
      else skip;
    }
} with store
   

function reset (const store : storage) : storage is
block {
    const empty_set : set (address) = Set.empty;
    // check if the owner of the contract is trying to reset -> if True then reset the value
    if sender = owner and store.status = False then 
        store := store with record [
          status = True;
          oui = 0n;
          non = 0n;
          voters = empty_set;
        ]
    else failwith("Acces denied.")
  
} with store

function main (const action : parameter; const store : storage): return is
block {
  const new_storage : storage = case action of
    | Vote (n) -> vote (n, store)
    | Reset -> reset (store)
    | Stdby (n) -> break (n, store)
  end
} with ((nil : list (operation)), new_storage)
  