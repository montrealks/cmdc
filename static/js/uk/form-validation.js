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
      PropertyValue: "required",
      LoanAmount: "required",
      LoanPurpose: "required",
      FoundProperty: "required",
      MadeOffer: "required",
      PurchaseTimeFrame: "required",
      EmploymentStatus: "required",
      ProveIncome: "required",
      AnyOtherDebt: "required",
      BirthDate: "required",
      CreditRating: "required",
      FirstName: "required",
      Surname: "required",
      Address: "required",
      Postcode: "required",
      tcpa_disclosure: "required",
      EmailAddress: {
        required: true,
        // Specify that email should be validated
        // by the built-in "email" rule
        email: true
      },
      PhoneNumber: {
        required: true,
        phoneUK: true
      },
      Mobile: {
        required: true,
        phoneUK: true
      }
    },
    // Specify validation error messages
    messages: {
      LoanType: "What type of loan are you applying for?",
      PropertyValue: "What is the current property value?",
      LoanAmount: "How much do you want to borrow?",
      LoanPurpose: "Purpose for wanting the mortgage?",
      FoundProperty: "Found a property you want to buy?",
      MadeOffer: "Have you put in an offer?",
      PurchaseTimeFrame: "What is your purchase time frame?",
      EmploymentStatus: "What is you employment status?",
      ProveIncome: "Can you prove your income?",
      AnyOtherDebt: "Do you have any other debt?",
      BirthDate: "Please enter your Date of Birth",
      CreditRating: "How is your credit history?",
      FirstName: "Please enter your First Name",
      Surname: "Please enter your Surname",
      Address: "Please enter your Address",
      Postcode: "Please enter your Postcode",
      PhoneNumber: "Please enter a valid UK Phone Number",
      Mobile: "Please enter a valid UK Phone Number",
      tcpa_disclosure: "You must consent to submit this form.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;",
      EmailAddress: "Please enter a valid Email Address"
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
    submitHandler: function(form) {
      form.submit();
    }
  });
});