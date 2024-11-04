import discord, io
from datetime import datetime
from discord.ext import commands
from typing import Any, Callable, Iterable, cast, Type, TypeVar


class Helper:
    PREFIX_MENTION_SYMBOL = "@"

    @classmethod
    def prefix_is_mention(cls, prefix: str) -> bool:
        return prefix == cls.PREFIX_MENTION_SYMBOL

    @classmethod
    def prefixes_has_mention(cls, prefixes: Iterable[str]) -> bool:
        return cls.PREFIX_MENTION_SYMBOL in prefixes


class an:
    @staticmethod
    def activity(
        activity_type: discord.ActivityType, name: str, **kwargs
    ) -> discord.BaseActivity:
        """Creates and returns a Discord Activity object (any subclass of BaseActivity)."""

        match (activity_type):
            case discord.ActivityType.playing:
                created_activity = discord.Game(name=name)
            case discord.ActivityType.streaming:
                created_activity = discord.Streaming(
                    name=name,
                    url=kwargs.get("url", "https://www.youtube.com/TheLivingPepsi"),
                )
            case discord.ActivityType.custom:
                created_activity = discord.CustomActivity(name=name)
            case _:
                created_activity = discord.Activity(
                    type=activity_type,
                    name=name,
                    state=kwargs.get("state"),
                )

        return created_activity

    @staticmethod
    def allowed_mentions(
        *permissions,
    ) -> discord.AllowedMentions:
        """Creates and returns an AllowedMentions object."""

        if "all" in permissions:
            return discord.AllowedMentions.all()
        elif "none" in permissions or len(permissions) == 0:
            return discord.AllowedMentions.none()

        return discord.AllowedMentions(
            everyone="everyone" in permissions,
            users="users" in permissions,
            roles="roles" in permissions,
            replied_user="replied_user" in permissions,
        )

    @staticmethod
    def prefix(
        *prefixes: str,
    ) -> Iterable[str] | str | Callable[[commands.Bot, discord.Message], list[str]]:
        """Creates and returns values that are prefixes for Discord bots."""

        if type(prefixes) == str:
            if Helper.prefix_is_mention(prefixes):
                return commands.when_mentioned
        else:
            if len(prefixes) >= 2 and Helper.prefixes_has_mention(prefixes):
                return commands.when_mentioned_or(*prefixes)
            elif len(prefixes) == 1 and Helper.prefixes_has_mention(prefixes):
                return commands.when_mentioned

        return prefixes

    @staticmethod
    def intents(*permissions: str) -> discord.Intents:
        """Creates and returns an Intents object."""

        if "all" in permissions:
            return discord.Intents.all()
        elif "default" in permissions:
            return discord.Intents.default()
        elif "none" in permissions:
            return discord.Intents.none()

        return discord.Intents(
            guilds="guilds" in permissions,
            members="members" in permissions,
            moderation="moderation" in permissions or "bans" in permissions,
            emojis_and_stickers="emojis_and_stickers" in permissions
            or "emojis" in permissions,
            integrations="integrations" in permissions,
            webhooks="webhooks" in permissions,
            invites="invites" in permissions,
            voice_states="voice_states" in permissions,
            presences="presences" in permissions,
            guild_messages="guild_messages" in permissions or "messages" in permissions,
            dm_messages="dm_messages" in permissions or "messages" in permissions,
            guild_reactions="guild_reactions" in permissions
            or "reactions" in permissions,
            dm_reactions="dm_reactions" in permissions or "reactions" in permissions,
            guild_typing="guild_typing" in permissions or "typing" in permissions,
            dm_typing="dm_typing" in permissions or "typing" in permissions,
            message_content="message_content" in permissions,
            guild_scheduled_events="guild_scheduled_events" in permissions,
            auto_moderation_configuration="auto_moderation_configuration" in permissions
            or "auto_moderation" in permissions,
            auto_moderation_execution="auto_moderation_execution" in permissions
            or "auto_moderation" in permissions,
            guild_polls="guild_polls" in permissions or "polls" in permissions,
            dm_polls="dm_polls" in permissions or "polls" in permissions,
        )

    @staticmethod
    def formatted_time(seconds: int | float | None = None) -> str:
        """Returns the given seconds in the HH:MM:SS format. If seconds is not greater than or equal to 1 hour, the hour is dropped from the format."""

        if seconds is None:
            return "0"

        hours, remaining_seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(remaining_seconds, 60)

        hour = f"{hours:02d}:" if hours > 0 else ""
        timestamp = f"{minutes:02d}:{seconds:02d}"

        formatted = f"{hour}{timestamp}"

        return formatted

    @classmethod
    def embed(
        cls,
        from_dict: dict[str, str] | None = None,
        *,
        title: str | None = None,
        description: str | None = None,
        url: str | None = None,
        timestamp: datetime | None = None,
        color: discord.Color | None = None,
        footer: dict[str, str] | None = None,
        image: str | None = None,
        thumbnail: str | None = None,
        author: dict[str, str] | None = None,
        fields: list[dict[str, str | bool | int]] | None = None,
    ):
        """Creates and returns a Discord Embed object."""

        if from_dict is not None:
            return discord.Embed.from_dict(from_dict)

        if isinstance(title, str) and len(title) > 256:
            title = title[:256]

        if isinstance(description, str) and len(description) > 4096:
            description = description[:4096]

        new_embed = discord.Embed(
            title=title,
            description=description,
            url=url,
            timestamp=timestamp,
            color=color,
        )

        if footer:
            footer_text = footer.get("text")

            if isinstance(footer_text, str) and len(footer_text) > 2048:
                footer_text = footer_text[:2048]

            new_embed.set_footer(
                text=footer_text,
                icon_url=footer.get("icon_url", footer.get("url")),
            )

        if image:
            new_embed.set_image(url=image)

        if thumbnail:
            new_embed.set_thumbnail(url=thumbnail)

        if author:
            author_name = author.get("name")

            if isinstance(author_name, str) and len(author_name) > 256:
                author_name = author_name[:256]

            new_embed.set_author(
                name=author.get("name"),
                url=author.get("url"),
                icon_url=author.get("icon_url"),
            )

        if fields:
            for i, field in enumerate(fields):
                if i == 25:
                    break

                field_index = field.get("index")

                if not isinstance(field_index, int):
                    field_index = None

                field_name = field.get("name")

                if isinstance(field_name, str) and len(field_name) > 256:
                    field_name = field_name[:256]

                field_value = field.get("value")

                if isinstance(field_value, str) and len(field_value) > 1024:
                    field_value = field_value[:1024]

                if field_index:
                    new_embed.insert_field_at(
                        index=field_index,
                        name=field_name,
                        value=field_value,
                        inline=bool(field.get("inline")),
                    )
                    continue

                new_embed.add_field(
                    name=field_name,
                    value=field_value,
                    inline=bool(field.get("inline")),
                )

        return new_embed


a = an

# Updated


class with_HTTP:
    async def __bytes_from_url(
        self,
        url: str | None = None,
    ) -> io.BytesIO | None:
        """Creates and returns a binary stream of data."""
        if not url:
            return

        async with self.session.get(url) as resp:
            if resp.status != 200:
                return
            return io.BytesIO(await resp.read())

    async def discord_file(
        self,
        media: discord.Attachment | str | None = None,
        properties: dict[str, Any] = {},
    ) -> discord.File | None:
        """Creates and returns a Discord File object."""

        filename, description, is_spoiler, is_url = unpacked_props(
            properties, ("filename", "description", "is_spoiler", "is_url")
        )

        if type(media) == discord.Attachment:
            return await media.to_file(
                filename=filename, description=description, spoiler=is_spoiler
            )
        elif type(media) == str:
            data = None
            if is_url:
                data = await self.__bytes_from_url(media)
            else:
                data = open(media, "rb")

        if data:
            return discord.File(
                data, filename=filename, description=description, spoiler=is_spoiler
            )

    async def files(
        self,
        files: list[str] | dict[str, dict[str, Any]] | None = None,
        properties: dict = {},
    ) -> list[discord.File | None] | None:
        """Creates and returns a list of Discord File objects. If properties is given, it overrides any per-file properties given in files if files is a dict."""
        if type(files) == dict:
            return [
                await self.discord_file(d_file, properties or file_props)
                for d_file, file_props in files.items()
            ]
        elif type(files) == list:
            return [await self.discord_file(d_file, properties) for d_file in files]
