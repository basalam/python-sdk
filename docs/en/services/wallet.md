# Wallet Service

Manage user balances, expenses, and refunds with the Wallet Service. This service provides comprehensive functionality
for handling user financial operations: get user balance and transaction history, create and manage expenses, process
refunds, and handle credit-specific operations.

## Table of Contents

- [Wallet Methods](#wallet-methods)
- [Examples](#examples)

## Wallet Methods

### Methods

| Method                                                                | Description                         | Parameters                                                                    |
|-----------------------------------------------------------------------|-------------------------------------|-------------------------------------------------------------------------------|
| [`get_balance()`](#get-balance-example)                               | Get user's balance                  | `user_id`, `filters`, `x_operator_id`                                         |
| [`get_transactions()`](#get-transactions-example)                     | Get transaction history             | `user_id`, `page`, `per_page`, `x_operator_id`                                |
| [`create_expense()`](#create-expense-example)                         | Create an expense                   | `user_id`, `request`, `x_operator_id`                                         |
| [`create_expense_from_credit()`](#create-expense-from-credit-example) | Create expense from specific credit | `user_id`, `credit_id`, `request`, `x_operator_id`                            |
| [`get_expense()`](#get-expense-example)                               | Get expense details                 | `user_id`, `expense_id`, `x_operator_id`                                      |
| [`delete_expense()`](#delete-expense-example)                         | Delete/rollback expense             | `user_id`, `expense_id`, `rollback_reason_id`, `x_operator_id`                |
| [`get_expense_by_ref()`](#get-expense-by-ref-example)                 | Get expense by reference            | `user_id`, `reason_id`, `reference_id`, `x_operator_id`                       |
| [`delete_expense_by_ref()`](#delete-expense-by-ref-example)           | Delete expense by reference         | `user_id`, `reason_id`, `reference_id`, `rollback_reason_id`, `x_operator_id` |
| [`create_refund()`](#create-refund-example)                           | Process a refund                    | `request`, `x_operator_id`                                                    |
| [`can_rollback_refund()`](#can-rollback-refund-example)               | Check if refund can be rolled back  | `refund_reason`, `refund_reference_id`, `x_operator_id`                       |
| [`rollback_refund()`](#rollback-refund-example)                       | Rollback a refund                   | `request`, `x_operator_id`                                                    |

## Examples

### Basic Setup

```python
from basalam_sdk import BasalamClient, PersonalToken
from basalam_sdk.wallet.models import (
    SpendCreditRequest, SpendSpecificCreditRequest, RefundRequest,
    RollbackRefundRequest, BalanceFilter
)

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Get Balance Example

```python
async def get_balance_example():
    balance = await client.get_balance(
        user_id=123,
        filters=[
            BalanceFilter(
                cash=True,
                settleable=True,
                vendor=False,
                customer=True
            )
        ],
        x_operator_id=456
    )
    
    print(f"User balance: {balance}")
    return balance
```

### Get Transactions Example

```python
async def get_transactions_example():
    transactions = await client.get_transactions(
        user_id=123,
        page=1,
        per_page=20,
        x_operator_id=456
    )
    
    for transaction in transactions.data:
        print(f"Transaction: {transaction.time} - Amount: {transaction.amount}")
    
    return transactions
```

### Create Expense Example

```python
async def create_expense_example():
    expense = await client.create_expense(
        user_id=123,
        request=SpendCreditRequest(
            reason_id=1,
            reference_id=456,
            amount=10000,
            description="Payment for order #456",
            types=[1, 2],
            settleable=True,
            references={
                "order_id": 456,
                "payment_method": 1
            }
        ),
        x_operator_id=456
    )
    
    print(f"Expense created: {expense.id}")
    return expense
```

### Create Expense From Credit Example

```python
async def create_expense_from_credit_example():
    expense = await client.create_expense_from_credit(
        user_id=123,
        credit_id=789,
        request=SpendSpecificCreditRequest(
            reason_id=1,
            reference_id=456,
            amount=5000,
            description="Payment from specific credit",
            settleable=True,
            references={
                "order_id": 456,
                "credit_type": 1
            }
        ),
        x_operator_id=456
    )
    
    print(f"Specific credit expense created: {expense.id}")
    return expense
```

### Get Expense Example

```python
async def get_expense_example():
    expense = await client.get_expense(
        user_id=123,
        expense_id=456,
        x_operator_id=456
    )
    
    print(f"Expense amount: {expense.amount}")
    print(f"Expense description: {expense.description}")
    
    return expense
```

### Delete Expense Example

```python
async def delete_expense_example():
    result = await client.delete_expense(
        user_id=123,
        expense_id=456,
        rollback_reason_id=2,
        x_operator_id=456
    )
    
    print(f"Expense deleted: {result.id}")
    return result
```

### Get Expense By Ref Example

```python
async def get_expense_by_ref_example():
    expense = await client.get_expense_by_ref(
        user_id=123,
        reason_id=1,
        reference_id=456,
        x_operator_id=456
    )
    
    if expense:
        print(f"Found expense: {expense.id}")
    return expense
```

### Delete Expense By Ref Example

```python
async def delete_expense_by_ref_example():
    result = await client.delete_expense_by_ref(
        user_id=123,
        reason_id=1,
        reference_id=456,
        rollback_reason_id=2,
        x_operator_id=456
    )
    
    print(f"Expense deleted by reference: {result.id}")
    return result
```

### Create Refund Example

```python
async def create_refund_example():
    refund = await client.create_refund(
        request=RefundRequest(
            original_reason=1,
            original_reference_id=456,
            reason=2,
            reference_id=789,
            amount=5000,
            description="Refund for cancelled order",
            references=[
                {
                    "reference_type_id": 1,
                    "reference_id": 456
                }
            ]
        ),
        x_operator_id=456
    )
    
    print(f"Refund processed: {refund.id}")
    return refund
```

### Can Rollback Refund Example

```python
async def can_rollback_refund_example():
    can_rollback = await client.can_rollback_refund(
        refund_reason=2,
        refund_reference_id=789,
        x_operator_id=456
    )
    
    print(f"Can rollback refund: {can_rollback.status}")
    print(f"Message: {can_rollback.message}")
    
    return can_rollback
```

### Rollback Refund Example

```python
async def rollback_refund_example():
    result = await client.rollback_refund(
        request=RollbackRefundRequest(
            refund_reason=2,
            rollback_refund_reason=3,
            refund_reference_id=789,
            reference_id=456,
            description="Rollback refund due to error",
            references=[
                {
                    "reference_type_id": 1,
                    "reference_id": 456
                }
            ]
        ),
        x_operator_id=456
    )
    
    print(f"Refund rolled back: {result.id}")
    return result
```

## Next Steps

- [Webhook Service](./webhook.md) - Handle webhook subscriptions
- [Chat Service](./chat.md) - Messaging and chat functionalities
- [Order Service](./order.md) - Manage orders and payments 
