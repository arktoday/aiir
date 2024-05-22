
from access.models import Operation


class OperationsService:
    def create_operation(self) -> Operation:
        operation = Operation()
        operation.save()
        
        return operation

    def finish_operation(self, id: int, result):
        operation = Operation.objects.get(id=id)
        
        if not operation:
            return False
        
        operation.result = result
        operation.done = True
        operation.save()

    def get_operation(self, id: int) -> Operation:
        operation = Operation.objects.get(id=id)
        
        if not operation:
            return False
        
        return operation
