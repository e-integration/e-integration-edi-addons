
openerp.eintegration_edi_manager = function(instance, local) {
	var QWeb = instance.web.qweb;
	var _t = instance.web._t;

	local.FieldSelection = instance.web.form.FieldChar.extend({
		init: function (field_manager, node) {
	        this._super(field_manager, node);
	    },
		start: function() {
			var self = this;
			this.$el.append(QWeb.render("export_widget_button"));
	        this.$("button#bselect").click(function() {
	        	self.show_selection();
	        });
	        self.$el.find('#export_div').html(QWeb.render("fields_export"));
    		self.bind_events();
	    },
	    bind_events: function() {
	    	var self = this;
	    	self.$el.find('#add_field').click(function() {
	    		self.$el.find('#field-tree-structure tr.ui-selected')
	                .removeClass('ui-selected')
	                .find('a').each(function () {
	                    var id = $(this).attr('id').split('-')[1];
	                    var string = $(this).attr('string');
	                    self.add_field(id, string);
                });
	    	});
	    	self.$el.find('#remove_field').click(function() {
	    		self.$el.find('#fields_list option:selected').remove();
	    	});
	    	self.$el.find('#remove_all_field').click(function() {
	    		self.$el.find('#fields_list').empty();
	    	});
	    	self.$el.find('#export_fields').click(function() {
	    		self.export_fields();
	    	});
	    	self.$el.find('#hide_fields').click(function() {
	    		self.hide_selection();
	    	});
	    },
	    get_stored_fields: function() {
	    	var self = this;
	    	if (self.field_manager.datarecord.export_field_ids){
	    		self.rpc('/edi_manager/get_stored_fields', {
	    			export_field_ids: self.field_manager.datarecord.export_field_ids
	    			}).done(function(records) {
	    				_.each(records, function(record) {self.add_field(record.name, record.label)});
	    		})
	    	}
	    },
	    export_fields: function() {
	    	var self = this;
	    	var exported_fields = this.$el.find('#fields_list option').map(function () {
	            return {field_name: this.value, field_label: this.textContent || this.innerText}
	        }).get();
	    	self.rpc("/edi_manager/export_fields", {
                data: exported_fields,
                record_id: self.field_manager.datarecord.id
            }).done(function() {
            	location.reload(true);
            });
	    },
	    show_selection: function() {
	    	var self = this;
	    	var got_fields = new $.Deferred();
	    	if (self.field_manager.datarecord.hasOwnProperty("id")) {
	    		self.rpc("/edi_manager/get_fields", {
	  	          model: self.field_manager.datarecord.model_name,
	  	          import_compat: false,
	  		      }).done(function (records) {
	  		          got_fields.resolve();
	  		          self.on_show_data(records);
	  		          self.get_stored_fields();
	  		      });
	  	    	$("#export_div").show();
	    	}
	    },
	    on_click: function(id, record) {
	        var self = this;
	        if (!record['children']) {
	            return;
	        }
	        var model = record['params']['model'],
	            prefix = record['params']['prefix'],
	            name = record['params']['name'],
	            exclude_fields = [];
	        if (record['relation_field']) {
	            exclude_fields.push(record['relation_field']);
	        }

	        if (!record.loaded) {
	            var import_comp = self.$el.find("#import_compat").val();
	            self.rpc("/edi_manager/get_fields", {
	                model: model,
	                prefix: prefix,
	                parent_name: name,
	                import_compat: Boolean(import_comp),
	                parent_field_type : record['field_type'],
	                exclude: exclude_fields
	            }).done(function(results) {
	                record.loaded = true;
	                self.on_show_data(results, record.id);
	            });
	        } else {
	            self.showcontent(record.id);
	        }
	    },
	    showcontent: function(id) {
	        // show & hide the contents
	        var $this = this.$el.find("tr[id='treerow-" + id + "']");
	        var is_open = $this.hasClass('open');
	        $this.toggleClass('open');

	        var first_child = $this.find('img');
	        if (is_open) {
	            first_child.attr('src', '/web/static/src/img/expand.gif');
	        } else {
	            first_child.attr('src', '/web/static/src/img/collapse.gif');
	        }
	        var child_field = this.$el.find("tr[id^='treerow-" + id +"/']");
	        var child_len = (id.split("/")).length + 1;
	        for (var i = 0; i < child_field.length; i++) {
	            var $child = $(child_field[i]);
	            if (is_open) {
	                $child.hide();
	            } else if (child_len == (child_field[i].id.split("/")).length) {
	                if ($child.hasClass('open')) {
	                    $child.removeClass('open');
	                    $child.find('img').attr('src', '/web/static/src/img/expand.gif');
	                }
	                $child.show();
	            }
	        }
	    },
	    on_show_data: function(result, after) {
	        var self = this;
	        if (after) {
	            var current_tr = self.$el.find("tr[id='treerow-" + after + "']");
	            current_tr.addClass('open');
	            current_tr.find('img').attr('src','/web/static/src/img/collapse.gif');
	            current_tr.after(QWeb.render('object_fields_tree.children', {'fields': result}));
	        } else {
	            self.$el.find('#left_field_panel').append(QWeb.render('object_fields_tree', {'fields': result}));
	        }
	        _.each(result, function(record) {
	            if (record.required) {
	                var required_fld = self.$el.find("tr[id='treerow-" + record.id + "']").find('#tree-column');
	                required_fld.addClass("oe_export_requiredfield");
	            }
	            self.$el.find("img[id='parentimg-" + record.id +"']").click(function() {
	                self.on_click(this.id, record);
	            });

	            self.$el.find("tr[id='treerow-" + record.id + "']").click(function(e) {
	                if (e.shiftKey) {
	                    var frst_click, scnd_click = '';
	                    if (self.row_index === 0) {
	                        self.row_index = this.rowIndex;
	                        frst_click = self.$el.find("tr[id^='treerow-']")[self.row_index-1];
	                        $(frst_click).addClass("ui-selected");
	                    } else {
	                        var i;
	                        if (this.rowIndex >=self.row_index) {
	                            for (i = (self.row_index-1); i < this.rowIndex; i++) {
	                                scnd_click = self.$el.find("tr[id^='treerow-']")[i];
	                                if (!$(scnd_click).find('#tree-column').hasClass("oe_export_readonlyfield")) {
	                                    $(scnd_click).addClass("ui-selected");
	                                }
	                            }
	                        } else {
	                            for (i = (self.row_index-1); i >= (this.rowIndex-1); i--) {
	                                scnd_click = self.$el.find("tr[id^='treerow-']")[i];
	                                if (!$(scnd_click).find('#tree-column').hasClass("oe_export_readonlyfield")) {
	                                    $(scnd_click).addClass("ui-selected");
	                                }
	                            }
	                        }
	                    }
	                }
	                self.row_index = this.rowIndex;

	                self.$el.find("tr[id='treerow-" + record.id + "']").keyup(function() {
	                    self.row_index = 0;
	                });
	                var o2m_selection = self.$el.find("tr[id='treerow-" + record.id + "']").find('#tree-column');
	                if ($(o2m_selection).hasClass("oe_export_readonlyfield")) {
	                    return false;
	                }
	                if (e.ctrlKey) {
	                    if ($(this).hasClass('ui-selected')) {
	                        $(this).removeClass('ui-selected').find('a').blur();
	                    } else {
	                        $(this).addClass('ui-selected').find('a').focus();
	                    }
	                } else if (!e.shiftKey) {
	                    self.$el.find("tr.ui-selected")
	                            .removeClass("ui-selected").find('a').blur();
	                    $(this).addClass("ui-selected").find('a').focus();
	                }
	                return false;
	            });

	            self.$el.find("tr[id='treerow-" + record.id + "']").keydown(function(e) {
	                var keyCode = e.keyCode || e.which;
	                var arrow = {left: 37, up: 38, right: 39, down: 40 };
	                var elem;
	                switch (keyCode) {
	                    case arrow.left:
	                        if ($(this).hasClass('open')) {
	                            self.on_click(this.id, record);
	                        }
	                        break;
	                    case arrow.right:
	                        if (!$(this).hasClass('open')) {
	                            self.on_click(this.id, record);
	                        }
	                        break;
	                    case arrow.up:
	                        elem = this;
	                        $(elem).removeClass("ui-selected");
	                        while (!$(elem).prev().is(":visible")) {
	                            elem = $(elem).prev();
	                        }
	                        if (!$(elem).prev().find('#tree-column').hasClass("oe_export_readonlyfield")) {
	                            $(elem).prev().addClass("ui-selected");
	                        }
	                        $(elem).prev().find('a').focus();
	                        break;
	                    case arrow.down:
	                        elem = this;
	                        $(elem).removeClass("ui-selected");
	                        while(!$(elem).next().is(":visible")) {
	                            elem = $(elem).next();
	                        }
	                        if (!$(elem).next().find('#tree-column').hasClass("oe_export_readonlyfield")) {
	                            $(elem).next().addClass("ui-selected");
	                        }
	                        $(elem).next().find('a').focus();
	                        break;
	                }
	            });
	            self.$el.find("tr[id='treerow-" + record.id + "']").dblclick(function() {
	                var $o2m_selection = self.$el.find("tr[id^='treerow-" + record.id + "']").find('#tree-column');
	                if (!$o2m_selection.hasClass("oe_export_readonlyfield")) {
	                   self.add_field(record.id, $(this).find("a").attr("string"));
	                }
	            });
	        });
	        self.$el.find('#fields_list').mouseover(function(event) {
	            if (event.relatedTarget) {
	                if (event.relatedTarget.attributes['id'] && event.relatedTarget.attributes['string']) {
	                    var field_id = event.relatedTarget.attributes["id"]["value"];
	                    if (field_id && field_id.split("-")[0] === 'export') {
	                        if (!self.$el.find("tr[id='treerow-" + field_id.split("-")[1] + "']").find('#tree-column').hasClass("oe_export_readonlyfield")) {
	                            self.add_field(field_id.split("-")[1], event.relatedTarget.attributes["string"]["value"]);
	                        }
	                    }
	                }
	            }
	        });
	    },
	    add_field: function(field_id, string) {
	        var field_list = this.$el.find('#fields_list');
	        if (this.$el.find("#fields_list option[value='" + field_id + "']")
	                && !this.$el.find("#fields_list option[value='" + field_id + "']").length) {
	            field_list.append(new Option(string, field_id));
	        }
	    },
	    hide_selection: function(widget) {
	    	$("#export_div").hide();
	    }
	});

	instance.web.form.widgets.add('FieldSelection', 'instance.eintegration_edi_manager.FieldSelection');
};