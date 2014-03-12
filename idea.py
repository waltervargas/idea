from osv import osv, fields

class idea(osv.model):
    _name = 'idea.idea'
    _columns = {
        'name': fields.char(
            'Title',
            size=64,
            require=True,
            translate=True
        ),
        'state': fields.selection(
            [('draft','Draft'),
             ('confirmed','Confirmed')],
            'State',
            required=True,
            readonly=True
        ),
        # Description is read-only when not draft !
        'description': fields.text(
            'Description',
            readonly=True,
            states=('draft': [('readonly', False)]),
            
        ),
        'active': fields.boolean('Active'),
        'invent_date': fields.date('Invent date'),

        # By convention, many2one to one fields end with _id
        'inventor_id': fields.many2one(
            'res.partner',
            'Inventor'
        ),

        'inventor_country_id': fields.related(
            'inventor_id',
            'country',
            readonly=True,
            type='many2one',
            relation='res.country',
            string='Country'
        ),

        # By convention, *2many fields end with _ids
        'vote_ids': fields.one2many(
            'idea.vote',
            'idea_id',
            'Votes'
        ),

        'sponsor_ids': fields.many2many(
            'res.partner',
            'idea_sponsor_rel',
            'idea_id',
            'sponsor_id',
            'Sponsors'
        ),
        'score': fields.float('Score',digits=(2,1)),

        'category_id': fields.many2one('idea.category','Category'),
            
    }

    _defaults = {
        'active' = True,
        'state' = 'draft',
    }

    def _check_name (self,cr,uid,ids):
        for idea in self.browse(cr, uid, ids):
            if 'spam' in idea.name: return False
        return True
    _sql_constraints = [('name_uniq','unique(name)', 'Ideas must be unique!')]
    _constraints = [(_check_name, 'Please avoid spam in ideas !', ['name'])]
    
