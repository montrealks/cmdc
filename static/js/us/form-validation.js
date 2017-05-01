// Wait for the DOM to be ready
$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
  $("form[name='quote']").validate({
    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      LoanType: "required",
      CurrentLoanType: "required",
      InterestRatePercentage: "required",
      PropertyType: "required",
      PropertyUse: "required",
      PropertyValue: "required",
      PurchaseYear: "required",
      PurchasePrice: "required",
      FirstTimeBuyer: "required",
      PurchaseTimeFrame: "required",
      DownPayment: "required",
      AnyMortgages: "required",
      FirstMortgageBalance: "required",
      SecondMortgage: "required",
      SecondMortgageBalance: "required",
      TotalMortgageBalance: "required",
      CashOutAmount: "required",
      AnyBankruptcy: "required",
      BankruptcyTime: "required",
      AnyForeclosure: "required",
      ForeclosureTime: "required",
      BehindOnPayments: "required",
      BirthDate: "required",
      CreditRating: "required",
      MilitaryOrVeteran: "required",
      FirstName: "required",
      LastName: "required",
      Address: "required",
      City: "required",
      State: "required",
      ZIPCode: "required",
      leadid_tcpa_disclosure: "required",
      EmailAddress: {
        required: true,
        // Specify that email should be validated
        // by the built-in "email" rule
        email: true
      },
      PhoneNumber: {
        required: true,
        phoneUS: true
      },
      DayPhoneNumber: {
        required: true,
        phoneUS: true
      }
    },
    // Specify validation error messages
    messages: {
      LoanType: "What type of loan are you applying for?",
      CurrentLoanType: "What is your current loan type?",
      InterestRatePercentage: "What is your current interest rate?",
      PropertyType: "What is the property type?",
      PropertyUse: "How will the property be used?",
      PropertyValue: "What is the current property value?",
      PurchaseYear: "What year did you purchase the property?",
      PurchasePrice: "What was the original purchase price of the property?",
      FirstTimeBuyer: "Are you a first time home buyer?",
      PurchaseTimeFrame: "What is your purchase time frame?",
      DownPayment: "What is your down payment percentage?",
      AnyMortgages: "Do you currently have any mortgages on the property?",
      FirstMortgageBalance: "What is your first mortgage balance?",
      SecondMortgage: "Do you have a second mortgage?",
      SecondMortgageBalance: "What is your second mortgage balance?",
      TotalMortgageBalance: "What is the combined balance of all of your mortgages?",
      CashOutAmount: "How much cash out are you requesting?",
      AnyBankruptcy: "Have you had any bankruptcies?",
      BankruptcyTime: "How long since your last bankruptcy?",
      AnyForeclosure: "Have you had any foreclosures?",
      ForeclosureTime: "How long since your last foreclosure?",
      BehindOnPayments: "Are you behind on payments?",
      BirthDate: "Please enter your Birth Date",
      CreditRating: "How would you rate your credit?",
      MilitaryOrVeteran: "Are you now or have you ever been in the military?",
      FirstName: "Please enter your First Name",
      LastName: "Please enter your Last Name",
      Address: "Please enter your Address",
      City: "Please enter your City",
      State: "Please select your State",
      ZIPCode: "Please enter your ZIP Code",
      PhoneNumber: "Please enter a valid US Phone Number (ex. 555-555-5555)",
      DayPhoneNumber: "Please enter a valid US Phone Number (ex. 555-555-5555)",
      leadid_tcpa_disclosure: "You must consent to submit this form.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;",
      EmailAddress: "Please enter a valid Email Address"
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
    submitHandler: function(form) {
      form.submit();
    }
  });
});