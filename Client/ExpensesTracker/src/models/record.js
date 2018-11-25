export default class record{
    constructor(
        ExpensesId,
        PaymentDate ,
        PaymentReason,
        PaymentValue,
        PaymentCurrencyId,
        CategoryId,
        UserId,
        CreatedAt,
        IsDeleted,
        IsIncome
    )
    {
        this.ExpensesId = ExpensesId
        this.PaymentDate  = PaymentDate 
        this.PaymentReason = PaymentReason
        this.PaymentValue = PaymentValue
        this.PaymentCurrencyId = PaymentCurrencyId
        this.CategoryId = CategoryId
        this.UserId = UserId
        this.CreatedAt = CreatedAt
        this.IsDeleted = IsDeleted
        this.IsIncome = IsIncome
    }
}