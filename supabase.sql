-- アニメ視聴検討表：投票用テーブルと関数
-- Supabase の SQL Editor にこのファイルの中身を貼り付けて「Run」を1回押してください。

create table if not exists public.votes (
  season     text        not null,
  title_id   int         not null,
  voter      uuid        not null,
  choice     text        not null check (choice in ('watch','maybe','skip')),
  updated_at timestamptz not null default now(),
  primary key (season, title_id, voter)
);

-- テーブルへの直接アクセスは禁止し、下の関数経由でのみ読み書きさせる
alter table public.votes enable row level security;
revoke all on public.votes from anon, authenticated;

-- 投票（同じ人が同じ作品に投票し直すと上書き。choice が null なら取り消し）
create or replace function public.cast_vote(p_season text, p_title int, p_voter uuid, p_choice text)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  if p_season !~ '^\d{4}-\d{2}$' or p_title < 1 or p_title > 500 then
    raise exception 'invalid input';
  end if;
  if p_choice is null then
    delete from votes where season = p_season and title_id = p_title and voter = p_voter;
  elsif p_choice in ('watch','maybe','skip') then
    insert into votes (season, title_id, voter, choice)
    values (p_season, p_title, p_voter, p_choice)
    on conflict (season, title_id, voter)
    do update set choice = excluded.choice, updated_at = now();
  else
    raise exception 'invalid choice';
  end if;
end;
$$;

-- 集計（作品ごとの票数）
create or replace function public.vote_counts(p_season text)
returns table (title_id int, watch bigint, maybe bigint, skip bigint)
language sql
stable
security definer
set search_path = public
as $$
  select title_id,
         count(*) filter (where choice = 'watch'),
         count(*) filter (where choice = 'maybe'),
         count(*) filter (where choice = 'skip')
  from votes
  where season = p_season
  group by title_id;
$$;

revoke all on function public.cast_vote(text,int,uuid,text) from public;
revoke all on function public.vote_counts(text) from public;
grant execute on function public.cast_vote(text,int,uuid,text) to anon, authenticated;
grant execute on function public.vote_counts(text) to anon, authenticated;
