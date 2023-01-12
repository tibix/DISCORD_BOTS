import discord
import datetime
import time
import platform

from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style
from typing import Optional


client = commands.Bot(command_prefix = ".", intents=discord.Intents.all())

# helper method to check if user is in a certain group
def is_admin(user):
    roles = [role.name for role in user.roles]
    if 'Developer' in roles or 'Community Heroes' in roles or 'Administrators' in roles:
        return True
    return False


# Initialize the BOT and print to stdout
@client.event
async def on_ready():
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET  + Fore.WHITE + Style.BRIGHT)
    print(prfx + " Logged in as " + Fore.YELLOW + client.user.name)
    print(prfx + " Bot ID " + Fore.YELLOW + str(client.user.id))
    print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + " Python Version " + Fore.YELLOW + platform.python_version())
    synced = await client.tree.sync()
    print(prfx + " Slash commands synced " + Fore.YELLOW + str(len(synced)) + " commands")


# Shut down the BOT
@client.tree.command(name="quit", description="Stops the bot")
async def shutdown(interaction: discord.Interaction):
    if is_admin(interaction.user):
        await interaction.response.send_message("TeeBee BOT is shutting down...")
        await client.close()
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, you are not allowed to run this command!")


# Get user info
@client.tree.command(name="uinfo", description="Show user info")
async def userinfo(interaction: discord.Interaction, member:discord.Member=None):
    if member == None:
        member = interaction.user
    embed = discord.Embed(title="User Info", description=f"Here's the user info on the user **{member.mention}**", color = discord.Color.green(), timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.display_avatar)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Name", value=f"{member.name}#{member.discriminator}")
    embed.add_field(name="Nickname", value=member.display_name)
    embed.add_field(name="Status", value=member.status)
    embed.add_field(name="Created At", value=member.created_at.strftime("%a, %B %#d, %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined At", value=member.joined_at.strftime("%a, %B %#d, %Y, %I:%M %p UTC"))
    embed.add_field(name=f"Roles ({len(member.roles)})", value=", ".join([role.mention for role in member.roles]))
    embed.add_field(name="Top Role", value=member.top_role.mention)
    embed.add_field(name="Messsages", value="0")
    embed.add_field(name='Bot?', value=member.bot)

    if is_admin(interaction.user):
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.sent_message(f'{interaction.user.mention} you are not allowed to run this command!')


# Get server info
@client.tree.command(name="serverinfo", description="Show info on the guild (a.k.a: server)")
async def serverinfo(interaction: discord.Interaction):
    embed = discord.Embed(title="Server info", description=f"Here's the server info on the server, {interaction.guild.name}", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=interaction.guild.icon)
    embed.add_field(name="Members", value=interaction.guild.member_count)
    embed.add_field(name="Channels", value=f"{len(interaction.guild.text_channels)} text | {len(interaction.guild.voice_channels)} voice")
    embed.add_field(name="Owner", value=interaction.guild.owner.mention)
    embed.add_field(name="Description", value=interaction.guild.description)
    embed.add_field(name="Create At", value=interaction.guild.created_at.strftime("%a, %B %#d, %Y, %I:%M %p UTC"))
    
    if is_admin(interaction.user):
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.sent_message(f'{interaction.user.mention} you are not allowed to run this command!')


# User prompt to explain
@client.tree.command(name="explain", description="Prompts user to explain the issue in detail")
async def explain(interaction: discord.Interaction):
    embed=discord.Embed(title="Explain your issue", description='To increase your chances of getting support from the community, please explain the issue in detail in more than a sentence.\n\nRemember: The people in the community give support for free!', color=discord.Color.dark_red())
    await interaction.response.send_message(embed=embed)


# CLPCTL Helper for root
@client.tree.command(name="clpctl_root", description="clpctl helper for root")
@app_commands.choices(subject=[
    app_commands.Choice(name="CloudFlare", value="cloudflare"),
    app_commands.Choice(name="CloudPanel", value="cloudpanel"),
    app_commands.Choice(name="DB", value="db"),
    app_commands.Choice(name="Lets-Encryypt", value="le"),
    app_commands.Choice(name="Site", value="site"),
    app_commands.Choice(name="System", value="system"),
    app_commands.Choice(name="User", value="user"),
    app_commands.Choice(name="VHOST Template", value="vhost-template"),
    app_commands.Choice(name="VHOST Templates", value="vhost-templates")])

async def clpctl_root(interaction:discord.Interaction, subject: Optional[app_commands.Choice[str]]):
    if (subject == None):
        embed = discord.Embed(title="Root CLI", description="**cloudflare**\n```clpctl cloudflare:update:ips```\n\n**cloudpanel**\n```clpctl cloudpanel:enable:basic-auth --userName=john.doe --password='password123'```\n```clpctl cloudpanel:disable:basic-auth```\n```clpctl cloudpanel:set:release-channel channel='test'```\n\n**db**\n```clpctl db:show:master-credentials```\n```clpctl db:add --domainName=www.domain.com --databaseName=my-database --databaseUserName=john --databaseUserPassword='!secretPassword!'```\n```clpctl db:export --databaseName=my-database --file=dump.sql.gz```\n```clpctl db:import --databaseName=my-database --file=dump.sql.gz```\n```clpctl db:delete --databaseName=my-database```\n\n**lets-encrypt**\n```clpctl lets-encrypt:install:certificate --domainName=www.domain.com--subjectAlternativeName=domain1.com,www.domain1.com```\n\n**site**\n**Adding a Node.js Site**\n```clpctl site:add:nodejs --domainName=www.domain.com --nodejsVersion=16 --appPort=3000 --siteUser=john --siteUserPassword='!secretPassword!'```\n**Adding a Static HTML Site**\n```clpctl site:add:static --domainName=www.domain.com --siteUser=john --siteUserPassword='!secretPassword!'```\n**Adding a PHP Site**\n```clpctl site:add:php --domainName=www.domain.com --phpVersion=8.1 --vhostTemplate='Generic' --siteUser=john --siteUserPassword='!secretPassword!'```**Adding a Python Site**\n```clpctl site:add:python --domainName=www.domain.com --pythonVersion=3.9 --appPort=8080 --siteUser=john --siteUserPassword='!secretPassword!'```\n**Deleting a site**\n```clpctl site:delete --domainName=www.domain.com```\n\n**system**\n```clpctl system:permissions:reset --directories=770 --files=660 --path=.```\n\n**user**\n```clpctl user:reset:password --userName=john.doe --password='!newPassword!'```\n```clpctl user:disable:mfa --userName=john.doe```\n\n**vhost-template**\n```clpctl vhost-template:add --name='My Application' --file=/tmp/template.tpl```\n```clpctl vhost-template:delete --name='My Application'```\n```clpctl vhost-template:view --name='My Application'```\n\n**vhost-templates**\n```clpctl vhost-templates:import```\n```clpctl vhost-templates:list```", color=discord.Color.yellow())
    elif (subject.value == 'cloudflare'):
        embed = discord.Embed(title="CLI: CloudFlare", description="```clpctl cloudflare:update:ips```", color=discord.Color.yellow())
    elif (subject.value == 'cloudpanel'):
        embed = discord.Embed(title="CLI: CLoudPanel", description="```clpctl cloudpanel:enable:basic-auth --userName=john.doe --password='password123'```\n```clpctl cloudpanel:disable:basic-auth```\n```clpctl cloudpanel:set:release-channel channel='test'```", color=discord.Color.yellow())
    elif (subject.value == 'db'):
        embed = discord.Embed(title="Root CLI: DB", description="```clpctl db:show:master-credentials```\n```clpctl db:add --domainName=www.domain.com --databaseName=my-database --databaseUserName=john --databaseUserPassword='!secretPassword!'```\n```clpctl db:export --databaseName=my-database --file=dump.sql.gz\nclpctl db:import --databaseName=my-database --file=dump.sql.gz```\n```clpctl db:delete --databaseName=my-database```", color=discord.Color.yellow())
    elif (subject.value == 'le'):
        embed = discord.Embed(title="Root CLI: Lets-Encrypt", description="```clpctl lets-encrypt:install:certificate --domainName=www.domain.com --subjectAlternativeName=domain1.com,www.domain1.com```", color=discord.Color.yellow())
    elif (subject.value == 'site'):
        embed = discord.Embed(title="Root CLI: Site", description="**Addding a NodeJS Site**\n```clpctl site:add:nodejs --domainName=www.domain.com --nodejsVersion=16 --appPort=3000 --siteUser=john --siteUserPassword='!secretPassword!'```\n\n**Adding a static site**\n```clpctl site:add:static --domainName=www.domain.com --siteUser=john --siteUserPassword='!secretPassword!'```\n\n**Adding a PHP Site**\n```clpctl site:add:php --domainName=www.domain.com --phpVersion=8.1 --vhostTemplate='Generic' --siteUser=john --siteUserPassword='!secretPassword!'```\n\n**Adding a Python Site**\n```clpctl site:add:python --domainName=www.domain.com --pythonVersion=3.9 --appPort=8080 --siteUser=john --siteUserPassword='!secretPassword!'```\n\n**Deleteing a Site**\n```clpctl site:delete --domainName=www.domain.com```", color=discord.Color.yellow())
    elif (subject.value == 'system'):
        embed = discord.Embed(title="Root CLI: System", description="```clpctl system:permissions:reset --directories=770 --files=660 --path=.```", color=discord.Color.yellow())
    elif (subject.value == 'user'):
        embed = discord.Embed(title="Root CLI: User", description="```clpctl user:reset:password --userName=john.doe --password='!newPassword!'```\n````clpctl user:disable:mfa --userName=john.doe```", color=discord.Color.yellow())
    elif (subject.value == 'vhost-template'):
        embed = discord.Embed(title="Root CLI: vhost-template", description="```clpctl vhost-template:add --name='My Application' --file=/tmp/template.tpl```\n```clpctl vhost-template:delete --name='My Application'```\n```clpctl vhost-template:view --name='My Application'```", color=discord.Color.yellow())
    elif (subject.value == 'vhost-templates'):
        embed = discord.Embed(title="Root CLI: vhost-templates", description="```clpctl vhost-templates:import```\n```clpctl vhost-templates:list```", color=discord.Color.yellow())
    await interaction.response.send_message(embed=embed)


# CLPCTL Helper for user
@client.tree.command(name="clpctl_user", description="clpctl helper for non-root users")
@app_commands.choices(subject=[
    app_commands.Choice(name="DB", value="db"),
    app_commands.Choice(name="System", value="system"),
    app_commands.Choice(name="Varnish Cache", value="varnish-cache")])

async def clpctl_user(interaction:discord.Interaction, subject: Optional[app_commands.Choice[str]]):
    if (subject == None):
        embed = discord.Embed(title="User CLI", description="**DB**\n```clpctl varnish-cache:purge --purge=all or --purge='tag1,tag2' or --purge='https://www.domain.com/site.html'```\n\n**System**\n```clpctl system:permissions:reset --directories=770 --files=660 --path=.```\n\n**Varnish-Cache**\n```clpctl varnish-cache:purge --purge=all or --purge='tag1,tag2' or --purge='https://www.domain.com/site.html'```", color=discord.Color.yellow())
    elif (subject.value == 'db'):
        embed = discord.Embed(title="User CLI: DB", description="```clpctl db:export --databaseName=my-database --file=dump.sql.gz```\n```clpctl db:import --databaseName=my-database --file=dump.sql.gz```", color=discord.Color.yellow())
    elif (subject.value == 'system'):
        embed = discord.Embed(title="User CLI: System", description="```clpctl system:permissions:reset --directories=770 --files=660 --path=.```", color=discord.Color.yellow())
    elif (subject.value == 'varnish-cache'):
        embed = discord.Embed(title="User CLI: Varnish-Cache", description="```clpctl varnish-cache:purge --purge=all or --purge='tag1,tag2' or --purge='https://www.domain.com/site.html'```", color=discord.Color.yellow())        
    await interaction.response.send_message(embed=embed)


# DOCS redirect based on subject
@client.tree.command(name="docs", description="give users a link to the online documentation based on a subject")
@app_commands.choices(subject=[
    app_commands.Choice(name="CloudPanel - Introduction", value="https://www.cloudpanel.io/docs/v2/introduction/"),
    app_commands.Choice(name="CloudPanel - Requirements", value="https://www.cloudpanel.io/docs/v2/requirements/"),
    app_commands.Choice(name="CloudPanel - Technology Stack", value="https://www.cloudpanel.io/docs/v2/technology-stack/"),
    app_commands.Choice(name="CloudPanel - Changelog", value="https://www.cloudpanel.io/docs/v2/changelog/"),
    app_commands.Choice(name="CloudPanel - Update", value="https://www.cloudpanel.io/docs/v2/update/"),
    app_commands.Choice(name="CloudPanel - Support", value="https://www.cloudpanel.io/docs/v2/support/"),
    app_commands.Choice(name="Getting Started - Installation - AWS AMI", value="https://www.cloudpanel.io/docs/v2/getting-started/amazon-web-services/installation/ami/"),
    app_commands.Choice(name="Getting Started - Installation - AWS Installer", value="https://www.cloudpanel.io/docs/v2/getting-started/amazon-web-services/installation/installer/"),
    app_commands.Choice(name="Getting Started - Installation - DO Marketplace", value="https://www.cloudpanel.io/docs/v2/getting-started/digital-ocean/installation/marketplace/"),
    app_commands.Choice(name="Getting Started - Installation - DO Installer", value="https://www.cloudpanel.io/docs/v2/getting-started/digital-ocean/installation/installer/"),
    app_commands.Choice(name="Getting Started - Installation - Hetzner Cloud Installer", value="https://www.cloudpanel.io/docs/v2/getting-started/hetzner-cloud/installation/installer/"),
    app_commands.Choice(name="Getting Started - Installation - Google Cloud Engine Installer", value="https://www.cloudpanel.io/docs/v2/getting-started/google-compute-engine/installation/installer/"),
    app_commands.Choice(name="Getting Started - Installation - Microsoft Azure Installer", value="https://www.cloudpanel.io/docs/v2/getting-started/microsoft-azure/installation/installer/"),
    app_commands.Choice(name="Getting Started - Installation - Vultr Marketplace", value="https://www.cloudpanel.io/docs/v2/getting-started/vultr/installation/marketplace/"),
    app_commands.Choice(name="Getting Started - Installation - Vultr Installer", value="https://www.cloudpanel.io/docs/v2/getting-started/vultr/installation/installer/"),
    app_commands.Choice(name="Getting Started - Installation - Other", value="https://www.cloudpanel.io/docs/v2/getting-started/other/"),
    app_commands.Choice(name="Front Area - Add Site", value="https://www.cloudpanel.io/docs/v2/frontend-area/add-site/"),
    app_commands.Choice(name="Front Area - Account", value="https://www.cloudpanel.io/docs/v2/frontend-area/account/"),
    app_commands.Choice(name="Front Area - Settings", value="https://www.cloudpanel.io/docs/v2/frontend-area/settings/"),
    app_commands.Choice(name="Front Area - Vhost", value="https://www.cloudpanel.io/docs/v2/frontend-area/vhost/"),
    app_commands.Choice(name="Front Area - Databases", value="https://www.cloudpanel.io/docs/v2/frontend-area/databases/"),
    app_commands.Choice(name="Front Area - Varnish Cache - Introduction", value="https://www.cloudpanel.io/docs/v2/frontend-area/varnish-cache/introduction/"),
    # app_commands.Choice(name="Front Area - Varnish Cache - Settings", value="https://www.cloudpanel.io/docs/v2/frontend-area/varnish-cache/settings/"),
    # app_commands.Choice(name="Front Area - Varnish Cache - Developer Guide - Vhost", value="https://www.cloudpanel.io/docs/v2/frontend-area/varnish-cache/developer-guide/vhost/"),
    # app_commands.Choice(name="Front Area - Varnish Cache - Developer Guide - PHP Controller", value="https://www.cloudpanel.io/docs/v2/frontend-area/varnish-cache/developer-guide/php-controller/"),
    # app_commands.Choice(name="Front Area - Varnish Cache - Migration", value="https://www.cloudpanel.io/docs/v2/frontend-area/varnish-cache/migration/"),
    # app_commands.Choice(name="Front Area - Varnish Cache - Service", value="https://www.cloudpanel.io/docs/v2/frontend-area/varnish-cache/service/"),
    # app_commands.Choice(name="Front Area - Varnish Cache - WordPress - Plugin", value="https://www.cloudpanel.io/docs/v2/frontend-area/varnish-cache/wordpress/plugin/"),
    # app_commands.Choice(name="Front Area - E-mail", value="https://www.cloudpanel.io/docs/v2/frontend-area/e-mail/"),
    # app_commands.Choice(name="Front Area - SSL/TLS", value="https://www.cloudpanel.io/docs/v2/frontend-area/tls/"),
    # app_commands.Choice(name="Front Area - Security", value="https://www.cloudpanel.io/docs/v2/frontend-area/security/"),
    # app_commands.Choice(name="Front Area - SSH/SFTP/FTP", value="https://www.cloudpanel.io/docs/v2/frontend-area/ssh-ftp/"),
    # app_commands.Choice(name="Front Area - File Manager", value="https://www.cloudpanel.io/docs/v2/frontend-area/file-manager/"),
    # app_commands.Choice(name="Front Area - Cron Jobs", value="https://www.cloudpanel.io/docs/v2/frontend-area/cron-jobs/"),
    # app_commands.Choice(name="Front Area - Logs", value="https://www.cloudpanel.io/docs/v2/frontend-area/logs/"),
    # app_commands.Choice(name="Admin Area - Users", value="https://www.cloudpanel.io/docs/v2/admin-area/users/"),
    # app_commands.Choice(name="Admin Area - Events", value="https://www.cloudpanel.io/docs/v2/admin-area/events/"),
    # app_commands.Choice(name="Admin Area - Instance", value="https://www.cloudpanel.io/docs/v2/admin-area/instance/"),
    # app_commands.Choice(name="Admin Area - Backups", value="https://www.cloudpanel.io/docs/v2/admin-area/backups/"),
    # app_commands.Choice(name="Admin Area - Security", value="https://www.cloudpanel.io/docs/v2/admin-area/security/"),
    # app_commands.Choice(name="Admin Area - Settings", value="https://www.cloudpanel.io/docs/v2/admin-area/settings/"),
    # app_commands.Choice(name="Admin Area - Cloud Features - AWS", value="https://www.cloudpanel.io/docs/v2/admin-area/cloud-features/amazon-web-services/"),
    # app_commands.Choice(name="Admin Area - Cloud Features - DO", value="https://www.cloudpanel.io/docs/v2/admin-area/cloud-features/digital-ocean/"),
    # app_commands.Choice(name="Admin Area - Cloud Features - Hetzner Cloud", value="https://www.cloudpanel.io/docs/v2/admin-area/cloud-features/hetzner-cloud/"),
    # app_commands.Choice(name="Admin Area - Cloud Features - Google Compute Engine", value="https://www.cloudpanel.io/docs/v2/admin-area/cloud-features/google-compute-engine/"),
    # app_commands.Choice(name="Admin Area - Cloud Features - Vultr", value="https://www.cloudpanel.io/docs/v2/admin-area/cloud-features/vultr/"),
    # app_commands.Choice(name="CloudPanel CLI - Root User Commands", value="https://www.cloudpanel.io/docs/v2/cloudpanel-cli/root-user-commands/"),
    # app_commands.Choice(name="CloudPanel CLI - Site User Commands", value="https://www.cloudpanel.io/docs/v2/cloudpanel-cli/site-user-commands/"),
    # app_commands.Choice(name="NodeJS - Deployment", value="https://www.cloudpanel.io/docs/v2/nodejs/deployment/pm2/"),
    # app_commands.Choice(name="NodeJS - Application - Ghost", value="https://www.cloudpanel.io/docs/v2/nodejs/applications/ghost/"),
    # app_commands.Choice(name="NodeJS - Application - Strapi 4", value="https://www.cloudpanel.io/docs/v2/nodejs/applications/strapi/"),
    # app_commands.Choice(name="PHP - Applications - Cake PHP", value="https://www.cloudpanel.io/docs/v2/php/applications/cakephp/"),
    # app_commands.Choice(name="PHP - Applications - CodeIgniter", value="https://www.cloudpanel.io/docs/v2/php/applications/codeigniter/"),
    # app_commands.Choice(name="PHP - Applications - Drupal", value="https://www.cloudpanel.io/docs/v2/php/applications/drupal/"),
    # app_commands.Choice(name="PHP - Applications - FuelPHP", value="https://www.cloudpanel.io/docs/v2/php/applications/fuelphp/"),
    # app_commands.Choice(name="PHP - Applications - Joomla", value="https://www.cloudpanel.io/docs/v2/php/applications/joomla/"),
    # app_commands.Choice(name="PHP - Applications - Laminas", value="https://www.cloudpanel.io/docs/v2/php/applications/laminas/"),
    # app_commands.Choice(name="PHP - Applications - Laravel", value="https://www.cloudpanel.io/docs/v2/php/applications/laravel/"),
    # app_commands.Choice(name="PHP - Applications - Magento", value="https://www.cloudpanel.io/docs/v2/php/applications/magento/"),
    # app_commands.Choice(name="PHP - Applications - Matomo", value="https://www.cloudpanel.io/docs/v2/php/applications/matomo/"),
    # app_commands.Choice(name="PHP - Applications - Mautic", value="https://www.cloudpanel.io/docs/v2/php/applications/mautic/"),
    # app_commands.Choice(name="PHP - Applications - Moodle", value="https://www.cloudpanel.io/docs/v2/php/applications/moodle/"),
    # app_commands.Choice(name="PHP - Applications - Neos", value="https://www.cloudpanel.io/docs/v2/php/applications/neos/"),
    # app_commands.Choice(name="PHP - Applications - Nextcloud", value="https://www.cloudpanel.io/docs/v2/php/applications/nextcloud/"),
    # app_commands.Choice(name="PHP - Applications - ownCloud", value="https://www.cloudpanel.io/docs/v2/php/applications/owncloud/"),
    # app_commands.Choice(name="PHP - Applications - PrestaShop", value="https://www.cloudpanel.io/docs/v2/php/applications/prestashop/"),
    # app_commands.Choice(name="PHP - Applications - Shopware", value="https://www.cloudpanel.io/docs/v2/php/applications/shopware/"),
    # app_commands.Choice(name="PHP - Applications - Slim", value="https://www.cloudpanel.io/docs/v2/php/applications/slim/"),
    # app_commands.Choice(name="PHP - Applications - Symfony", value="https://www.cloudpanel.io/docs/v2/php/applications/symfony/"),
    # app_commands.Choice(name="PHP - Applications - TYPO3", value="https://www.cloudpanel.io/docs/v2/php/applications/typo3/"),
    # app_commands.Choice(name="PHP - Applications - WooCommerce", value="https://www.cloudpanel.io/docs/v2/php/applications/woocommerce/"),
    # app_commands.Choice(name="PHP - Applications - WordPress", value="https://www.cloudpanel.io/docs/v2/php/applications/wordpress/"),
    # app_commands.Choice(name="PHP - Applications - Yii", value="https://www.cloudpanel.io/docs/v2/php/applications/yii/"),
    # app_commands.Choice(name="PHP - Applications - Other", value="https://www.cloudpanel.io/docs/v2/php/applications/other/"),
    # app_commands.Choice(name="PHP - Guides - Building a PHP Extension", value="https://www.cloudpanel.io/docs/v2/php/guides/building-a-php-extension/"),
    # app_commands.Choice(name="PHP - Guides - ionCube Loader", value="https://www.cloudpanel.io/docs/v2/php/guides/ioncube-loader/"),
    # app_commands.Choice(name="PHP - Guides - Node.js", value="https://www.cloudpanel.io/docs/v2/php/guides/nodejs/"),
    # app_commands.Choice(name="Python - Deployment - uwsgi", value="https://www.cloudpanel.io/docs/v2/python/deployment/uwsgi/"),
    # app_commands.Choice(name="Python - Guides - Adding a Python Version", value="https://www.cloudpanel.io/docs/v2/python/guides/adding-a-python-version/"),
    # app_commands.Choice(name="Guides - Best Practices - Migration - PHP Site", value="https://www.cloudpanel.io/docs/v2/guides/best-practices/migration/php-site/"),
    # app_commands.Choice(name="Guides - Security", value="https://www.cloudpanel.io/docs/v2/guides/best-practices/security/"),
    # app_commands.Choice(name="Guides - Performance - Server Benchmarks", value="https://www.cloudpanel.io/docs/v2/guides/best-practices/performance/server-benchmarks/"),
    # app_commands.Choice(name="Tools - WordPress - CLP E-Mail Sender From", value="https://www.cloudpanel.io/docs/v2/tools/wordpress/clp-email-sender-from/")
])

async def docs(interaction: discord.Integration, subject: Optional[app_commands.Choice[str]]):
    if not subject:
        embed = discord.Embed(title="CloudPanel Documentation", description="[Check out the documentation page](https://www.cloudpanel.io/docs/v2/)", color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=subject.name, description=f"{(subject.value)}", color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed)


TOKEN = "MTA0Mjc1NjE4NzkwMjQ0MzUzMQ.G_cRH9.z8LGR9vXao8EacOkQsXnedtnqSrAWE0UMttCCk"

client.run(TOKEN)

