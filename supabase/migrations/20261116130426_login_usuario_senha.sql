-- Login por usuário. O Auth continua com e-mail sintético.
-- Leo e Barbara acompanham. Jonas executa.

insert into public.role_invites (email, full_name, role) values
  ('leo@casa-control.local', 'Léo', 'manager'),
  ('barbara@casa-control.local', 'Bárbara', 'manager'),
  ('jonas@casa-control.local', 'Jonas', 'executor')
on conflict (email) do update
  set full_name = excluded.full_name,
      role = excluded.role;

update public.profiles as p
  set full_name = i.full_name,
      role = i.role
from public.role_invites as i
join auth.users as u on lower(u.email) = i.email
where p.id = u.id
  and i.email in (
    'leo@casa-control.local',
    'barbara@casa-control.local',
    'jonas@casa-control.local'
  );
