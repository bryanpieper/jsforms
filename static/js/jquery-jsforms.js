/*!
 * Django jsforms jQuery plugin
 * http://www.thepiepers.net/
 *
 * This plugin enables the JSON integration between the Django forms and the frontend.
 * 
 * Usage:
 *  <script type="text/javascript">
 *   $("form").jsform();
 *  </script>
 *
 * Copyright (c) 2011, Bryan Pieper
 * Released under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 */

(function($){

	$.fn.jsform = function(options) {
		// Default jsforms plugin settings. Can be override by
		// when attached.
		//
		// Example:
		//  $("form").jsform({ 'url': '/some/form/submit/', 'async':false });
		//  $("#anotherform form").jsform();
		// 
		// To hook into the success callback, provide a function instance as part
		// of the options named 'success'
		//  $("form").jsform({'requestSuccess': function() { console.log("completed request") }});
		var settings = {
			method: "POST",
			async: false,
			dataType: "json",
			url: undefined,
			cache: false,
			loaderElement: undefined,
			requestSuccess: undefined,
			requestError: undefined,
			data: function(form) {
				// Serializes the form as-is and ensures all fields
				// are included in submit
				return form.serialize();
			},
			preSubmit: function(form) {},
			// provide an error handler function if you wish to customize
			// the error behavior
			errorHandler: undefined,
			successHandler: undefined
		};
	
		return this.each(function() {
			if (options) { 
				$.extend(settings, options);
			}
			
			var $form = $(this);
			var actionUrl = (settings.url !== undefined ? settings.url : $form.attr("action"));
			if (!actionUrl) {
				if (typeof console !== "undefined") {
					console.log("Form does not have an 'action' attribute");
				}	
			}
			
			// Ajax loader show/hide logic
			var loader = {
				e: settings.loaderElement,
				show: function() {
					if (this.e) {
						$(this.e).show();
					}
				},
				hide: function() {
					if (this.e) {
						$(this.e).fadeOut("fast");
					}
				}
			};
			
			// Attach the submit event to the form
			$form.submit(function() {
				loader.show();
				
				if (typeof settings.preSubmit !== "undefined") {
					settings.preSubmit($form);
				}
				
				// Handles the successful response from the webserver
				var successCallback = function(data) {
					
					if (typeof settings.errorHandler === "undefined") {
						// Removes any leftover error elements
						$form.children(".error").removeClass("error").find("ul").remove();
						$form.children("ul.errorlist").remove();
					}

					if (typeof data.errors !== "undefined" && data.errors) {
						
						if (typeof settings.errorHandler === "undefined") {
							// Creates the error elements and adds appropriate .error 
							// classes to the form
							// 
							//  <div class=".field_name .field">
							//    <ul>
							//      <li>error msg 1</li>
							//      <li>error msg 2</li>
							//    </ul>
							//    <input name="field_name" type="text" id="id_field_name" />
							//  </div>
							// 
							// For the __all__ error case, will display the <ul> at end top of 
							// the form. Will have the 'errorlist' class
							for (var e in data.errors) {
								// The errors dict contains the names of the fields. Each contains
								// a list of the error messages. 
								var errors = data.errors;
								var ul = document.createElement("ul");
								for (var i=0; i<errors[e].length; i++) {
									var li = document.createElement("li");
									li.innerHTML = errors[e][i];
									ul.appendChild(li);
								}
								if (e == "__all__") {
									ul.className = "errorlist";
									$form.children().first().before(ul);
								} else {
									$form.children("." + e).addClass("error").children("label").before(ul);
								}
							}
						} else {
							// call the errorHandler for each field with errors
							for (var e in data.errors) {
								settings.errorHandler(e, data.errors[e]);
							}							
						}
						
					} else {
						if (typeof settings.successHandler === "undefined") {
							// Call the redirect if available
							if (typeof data.redirect && data.redirect) {
								window.location.href = data.redirect;
							}
						} else {
							// Call the successHanlder if no errors
							settings.successHandler(data);
						}
					}
					
					// Call the requestSuccess if Ajax call succeeded
					if (typeof settings.requestSuccess !== "undefined") {
						settings.requestSuccess(data);
					}
					
					loader.hide();
				};
				
				// Handles the unsuccessful response from the webserver
				var errorCallback = function(obj) {
					loader.hide();
					if (typeof settings.requestError !== "undefined") {
						settings.requestError(obj);
					}
				};
				
				var formData = settings.data($form);
				
				$.ajax({
					url: actionUrl,
					success: successCallback,
					error: errorCallback,
					async: settings.async,
					dataType: settings.dataType,
					data: formData,
					type: settings.method,
					cache: settings.cache
				});
				
				return false;
			});
			
		});
		
	};
})(jQuery);
