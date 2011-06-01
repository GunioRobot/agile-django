/*
 * @author: Andres Torres
 * Toolbar generator
 * GNU GPL v2
 * 14 July 2010
 * 
 */
jQuery(function($){
	$.fn.toolbar = function(settings){
		return this.each(function(){
			var $elem = $(this).addClass("toolbar fg-buttonset fg-buttonset-single")
			$.each(settings.buttons, function(i, val){
				var txt = "";
				val.extraClass = val.extraClass || '';
                
				if (typeof val === "undefined")
					return;
                
				if(val.uiIcon != undefined)
					txt = "<span class='ui-icon " + val.uiIcon + "'></span>";
                
				$("<button/>")
                .hover(function(){
                   $(this).addClass('ui-state-hover'); 
                }, function(){
                   $(this).removeClass('ui-state-hover'); 
                })
				.html(txt + val.name)
				.bind('click', val.click)
				.appendTo($elem)
				.addClass('fg-button ui-state-default ui-priority-primary ' + val.extraClass)
				.attr("id", val.id);

			});
            
			$elem.find('button')
			.first().addClass('ui-corner-left').end()
			.last().addClass('ui-corner-right').end();
			
		});
	}
});
