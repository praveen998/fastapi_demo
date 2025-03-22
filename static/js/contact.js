
function geturl() {
    url = localStorage.getItem("fasturl");
    return url;
}


$(document).ready(function() {
    // Initially hide the success message
//    $('#successMessage').hide();

    // On form submission
    // $('#contactForm').on('submit', function(event) {
    //     event.preventDefault(); // Prevent the default form submission

    //     // Initialize validation status
    //     let isValid = true;

    //     // Get form field values
    //     const name = $('#name').val().trim();
    //     const email = $('#email').val().trim();
    //     const message = $('#message').val().trim();
    //     alert(`${name},${email},${message}`);

        // $('#nameError').text('');
        // $('#emailError').text('');
        // $('#messageError').text('');

       
        // if (name === '') {
        //     $('#nameError').text('Name is required.');
        //     isValid = false;
        // }

       
        // const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        // if (email === '' || !emailRegex.test(email)) {
        //     $('#emailError').text('Enter a valid email address.');
        //     isValid = false;
        // }

    
        // if (message === '') {
        //     $('#messageError').text('Message cannot be empty.');
        //     isValid = false;
        // }

           
            // const feedbackData = {
            //     name: name,
            //     email: email,
            //     feedback: message
            // }

        
            // $('button[type="submit"]').prop('disabled', true).text('Sending...');

            // $.ajax({
            //     url: geturl()+'/send_feedback', 
            //     contentType: 'application/json',
            //     data: JSON.stringify(feedbackData),
            //     success: function(response) {
            //         console.log('Feedback sent successfully:', response);

                  
            //         $('#successMessage').fadeIn();

            //         // Reset form fields
            //         $('#contactForm')[0].reset();

            //         // Re-enable button and change text back
            //         $('button[type="submit"]').prop('disabled', false).text('Submit');

            //         // Hide success message after 5 seconds
            //         setTimeout(function() {
            //             $('#successMessage').fadeOut();
            //         }, 5000);
            //     },
            //     error: function(xhr, status, error) {
            //         console.error('Error sending feedback:', error);

            //         // Re-enable button
            //         $('button[type="submit"]').prop('disabled', false).text('Submit');

            //         alert('Oops! Something went wrong while sending your feedback.');
            //     }
            // });
//     });
 });


function validateForm() {
        
        const name = $('#name').val();
        const email = $('#email').val();
        const message = $('#message').val();
        alert(`${name},${email},${message}`);
        const feedbackData = {
                name: name,
                email: email,
                feedback: message
            }
              $.ajax({
                url: geturl()+'/send_feedback', 
                type: "POST",
                contentType: 'application/json',
                data: JSON.stringify(feedbackData),
                success: function(response) {
                    document.getElementById('successMessage').style.display = "block";
                    document.getElementById('contactForm').reset();
                
                },
                error: function(xhr, status, error) {
                  
                }
            });


        

    }



