from abc import ABC, abstractmethod

# Only types used here are T and U. 
# T == type of the item being stored, U == type of the id of the item being stored (usually UUID or int)
class Repository[T, U](ABC):
    @abstractmethod
    def store(self, incoming_item: T): 
        pass

    @abstractmethod
    def get_item(self, item_id: U) -> T:
        pass

    @abstractmethod
    def update_item(self, item_id: U, updated_item: T) -> T:
        pass

    @abstractmethod
    def delete_item(self, item_id: U) -> T:
        pass

    @abstractmethod
    def get_all_items(self) -> list[T]:
        pass