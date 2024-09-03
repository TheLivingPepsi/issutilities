import discord, io
from discord.ext import commands
from .client import HTTP
from typing import Any, Iterable, Callable, cast


def unpacked_props(
    props: dict[str, Any] = {}, mapped_values: Iterable[str] = []
) -> list[Any]:
    """Unpacks a properties dict into variables."""
    return [props.get(v) for v in mapped_values]


class an:
    def __init__(self) -> None:
        pass

    @classmethod
    def activity(
        cls, properties: dict[str, Any] = {"type": None}
    ) -> discord.Game | discord.Streaming | discord.Activity | None:
        """Creates and returns a Discord Activity object."""

        activity_type, activity_name, activity_url = unpacked_props(
            properties, ("type", "name", "url")
        )

        created_activity = None

        match (activity_type):
            case "Playing":
                created_activity = discord.Game(
                    name=(activity_name or "Something"),
                )

            case "Streaming":
                created_activity = discord.Streaming(
                    name=(activity_name or "Something"),
                    url=(activity_url or "https://www.twitch.tv/thelivingpepsi"),
                )

            case "Listening" | "Watching" | "Competing":
                created_activity = discord.Activity(
                    type=(
                        activity_type == "Competing"
                        and discord.ActivityType.competing
                        or activity_type == "Listening"
                        and discord.ActivityType.listening
                        or discord.ActivityType.watching
                    ),
                    name=(activity_name or "Something"),
                )

        return created_activity

    @classmethod
    def allowed_mentions(
        cls, properties: dict[str, bool] | str = "All"
    ) -> discord.AllowedMentions:
        """Creates and returns an AllowedMentions object."""
        AllowedMentions = discord.AllowedMentions

        reference = {
            "All": AllowedMentions.all(),
            "None": AllowedMentions.none(),
        }

        if type(properties) == dict:
            everyone, users, roles, replied_user = unpacked_props(
                properties, ("everyone", "users", "roles", "replied_user")
            )

            return discord.AllowedMentions(
                everyone=everyone, users=users, roles=roles, replied_user=replied_user
            )

        if properties in reference:
            return reference[properties]

        return reference["None"]

    @staticmethod
    def prefix(
        prefixes: list[str] = ["@"],
    ) -> list[str] | Callable[[None], list[str]]:
        """Creates and returns a list of prefixes."""
        prefix_mention, other_prefixes = False, False

        prefixes = cast(list[str], prefixes)

        for index, prefix in enumerate(prefixes):
            if prefix == "@":
                prefix_mention = True
                prefixes.pop(index)
            elif prefix_mention and other_prefixes:
                break
            else:
                other_prefixes = True

        if prefix_mention and other_prefixes:
            return cast(list[str], commands.when_mentioned_or(*prefixes))
        elif prefix_mention or not other_prefixes:
            return cast(list[str], commands.when_mentioned)
        return prefixes

    @staticmethod
    def intents(intent: dict[str, bool] | str = "All") -> discord.Intents:
        Intents = discord.Intents
        reference = {
            "All": Intents.all(),
            "Default": Intents.default(),
            "None": Intents.none(),
        }

        if type(intent) == str and intent in reference:
            return reference[intent]
        elif type(intent) == dict[str, bool]:
            return Intents(**intent)
        return reference["All"]

    @staticmethod
    def formatted_time(seconds: int | float | None = None) -> str:
        """Returns the given seconds in the HH:MM:SS format. If seconds is not greater than or equal to 1 hour, the hour is dropped from the format."""

        if not seconds:
            return "0"

        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        hour = f"{hours:02d}:" if hours > 0 else ""
        timestamp = f"{minutes:02d}:{seconds:02d}"

        formatted = f"{hour}{timestamp}"

        return formatted

    @classmethod
    def embed(cls, properties: dict[str, Any] = {}):
        """Creates and returns a Discord Embed object."""
        (
            title,
            description,
            url,
            timestamp,
            color,
            footer,
            image,
            thumbnail,
            author,
            fields,
        ) = unpacked_props(
            properties,
            (
                "title",
                "description",
                "url",
                "timestamp",
                "color",
                "footer",
                "image",
                "thumbnail",
                "author",
                "fields",
            ),
        )

        new_embed = discord.Embed(
            color=color,
            title=title,
            url=url,
            description=description,
            timestamp=timestamp,
        )

        if author:
            author_name, author_url, author_icon = unpacked_props(
                author, ("name", "url", "icon_url")
            )

            new_embed = new_embed.set_author(
                name=author_name, url=author_url, icon_url=author_icon
            )

        if footer:
            footer_text, footer_icon = unpacked_props(footer, ("text", "icon_url"))
            new_embed = new_embed.set_footer(text=footer_text, icon_url=footer_icon)

        if image:
            new_embed = new_embed.set_image(url=image)

        if thumbnail:
            new_embed = new_embed.set_thumbnail(url=thumbnail)

        if fields:
            for field in fields:
                field_index, field_name, field_value, field_inline = unpacked_props(
                    field, ("index", "name", "value", "inline")
                )

                if field_index:
                    new_embed = new_embed.insert_field_at(
                        index=field_index,
                        name=field_name,
                        value=field_value,
                        inline=field_inline,
                    )
                    continue

                new_embed = new_embed.add_field(
                    name=field_name, value=field_value, inline=field_inline
                )

        return new_embed


class a(an):
    pass


class with_HTTP(HTTP):
    def __init__(self) -> None:
        super().__init__()

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
