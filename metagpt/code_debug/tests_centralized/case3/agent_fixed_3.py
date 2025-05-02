@audioset.command()
@checks.mod_or_permissions(administrator=True)
async def thumbnail(self, ctx):
    """Toggle displaying a thumbnail on audio messages."""
    thumbnail = await self.config.guild(ctx.guild).thumbnail()
    await self.config.guild(ctx.guild).thumbnail.set(not thumbnail)
    await self._embed_msg(ctx, _("Thumbnail display: {}.").format(await self.config.guild(ctx.guild).thumbnail()))
